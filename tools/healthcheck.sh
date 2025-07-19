#!/bin/bash
#
# Wazuh MOPH Notify Integration Health Check Script
# Version: 2.0.0
#
# This script performs health checks for the MOPH Notify integration
# and logs the results for monitoring purposes.
#

# Configuration
LOG_FILE="/var/log/moph-notify-health.log"
INTEGRATION_SCRIPT="/var/ossec/integrations/custom-moph-notify.py"
WAZUH_SERVICE="wazuh-manager"
MOPH_API_URL="https://morpromt2f.moph.go.th"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log_message() {
    local level=$1
    local message=$2
    echo "[$DATE] $level: $message" >> "$LOG_FILE"
    
    case $level in
        "ERROR")
            echo -e "${RED}[$DATE] ERROR: $message${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}[$DATE] WARNING: $message${NC}"
            ;;
        "INFO")
            echo -e "${GREEN}[$DATE] INFO: $message${NC}"
            ;;
        *)
            echo "[$DATE] $level: $message"
            ;;
    esac
}

# Check if running as root or with proper permissions
check_permissions() {
    if [ "$EUID" -ne 0 ] && [ "$(id -gn)" != "wazuh" ]; then
        log_message "ERROR" "Script must be run as root or wazuh user"
        exit 1
    fi
}

# Check Wazuh Manager service
check_wazuh_service() {
    if systemctl is-active --quiet "$WAZUH_SERVICE"; then
        log_message "INFO" "Wazuh Manager service is running"
        return 0
    else
        log_message "ERROR" "Wazuh Manager service is not running"
        return 1
    fi
}

# Check integration files
check_integration_files() {
    local errors=0
    
    # Check Python script
    if [ -f "$INTEGRATION_SCRIPT" ]; then
        if [ -r "$INTEGRATION_SCRIPT" ]; then
            log_message "INFO" "Integration Python script found and readable"
        else
            log_message "ERROR" "Integration Python script not readable"
            errors=$((errors + 1))
        fi
    else
        log_message "ERROR" "Integration Python script not found: $INTEGRATION_SCRIPT"
        errors=$((errors + 1))
    fi
    
    # Check shell wrapper
    local shell_script="${INTEGRATION_SCRIPT%%.py}"
    if [ -f "$shell_script" ]; then
        if [ -x "$shell_script" ]; then
            log_message "INFO" "Integration shell script found and executable"
        else
            log_message "ERROR" "Integration shell script not executable"
            errors=$((errors + 1))
        fi
    else
        log_message "ERROR" "Integration shell script not found: $shell_script"
        errors=$((errors + 1))
    fi
    
    return $errors
}

# Check Python dependencies
check_python_dependencies() {
    local python_bin="/var/ossec/framework/python/bin/python3"
    local errors=0
    
    if [ -x "$python_bin" ]; then
        log_message "INFO" "Wazuh Python interpreter found"
        
        # Check required modules
        if $python_bin -c "import requests, json, sys; from datetime import datetime" 2>/dev/null; then
            log_message "INFO" "All required Python modules available"
        else
            log_message "ERROR" "Missing required Python modules"
            errors=$((errors + 1))
        fi
    else
        log_message "ERROR" "Wazuh Python interpreter not found or not executable"
        errors=$((errors + 1))
    fi
    
    return $errors
}

# Check configuration
check_configuration() {
    local errors=0
    
    # Check ossec.conf for integration
    if grep -q "custom-moph-notify" /var/ossec/etc/ossec.conf; then
        log_message "INFO" "MOPH Notify integration found in ossec.conf"
    else
        log_message "WARNING" "MOPH Notify integration not found in ossec.conf"
        errors=$((errors + 1))
    fi
    
    # Check API keys configuration
    if grep -q "YOUR_CLIENT_KEY\|YOUR_SECRET_KEY" "$INTEGRATION_SCRIPT"; then
        log_message "ERROR" "API keys not configured in integration script"
        errors=$((errors + 1))
    else
        log_message "INFO" "API keys appear to be configured"
    fi
    
    return $errors
}

# Check network connectivity
check_network() {
    local errors=0
    
    # Check DNS resolution
    if nslookup morpromt2f.moph.go.th >/dev/null 2>&1; then
        log_message "INFO" "DNS resolution for MOPH API successful"
    else
        log_message "WARNING" "DNS resolution for MOPH API failed"
        errors=$((errors + 1))
    fi
    
    # Check HTTPS connectivity
    if curl -s --max-time 10 --head "$MOPH_API_URL" >/dev/null 2>&1; then
        log_message "INFO" "HTTPS connectivity to MOPH API successful"
    else
        log_message "WARNING" "HTTPS connectivity to MOPH API failed"
        errors=$((errors + 1))
    fi
    
    return $errors
}

# Check log files and disk space
check_logs_and_disk() {
    local errors=0
    
    # Check log directory space
    local log_usage=$(df /var/ossec/logs | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$log_usage" -gt 90 ]; then
        log_message "WARNING" "Log directory usage is high: ${log_usage}%"
        errors=$((errors + 1))
    else
        log_message "INFO" "Log directory usage is normal: ${log_usage}%"
    fi
    
    # Check if integration logs exist
    if [ -f "/var/ossec/logs/integrations.log" ]; then
        log_message "INFO" "Integration log file exists"
    else
        log_message "INFO" "Integration log file not found (normal if no alerts sent)"
    fi
    
    return $errors
}

# Test integration with sample alert
test_integration() {
    local temp_alert="/tmp/health_check_alert_$$.json"
    local errors=0
    
    # Create sample alert
    cat > "$temp_alert" << 'EOF'
{
    "timestamp": "2025-07-18T10:30:00.000+0000",
    "rule": {
        "level": 5,
        "description": "Health check test alert",
        "id": "99999"
    },
    "agent": {
        "name": "health-check-agent"
    },
    "data": {
        "srcip": "127.0.0.1"
    }
}
EOF
    
    # Test script execution (dry run)
    if /var/ossec/framework/python/bin/python3 -c "
import sys; sys.path.insert(0, '/var/ossec/integrations');
exec(open('$INTEGRATION_SCRIPT').read())
" --help >/dev/null 2>&1; then
        log_message "INFO" "Integration script syntax check passed"
    else
        log_message "ERROR" "Integration script syntax check failed"
        errors=$((errors + 1))
    fi
    
    # Cleanup
    rm -f "$temp_alert"
    
    return $errors
}

# Main health check function
main() {
    log_message "INFO" "Starting MOPH Notify integration health check"
    
    local total_errors=0
    
    # Run all checks
    check_permissions
    
    check_wazuh_service
    total_errors=$((total_errors + $?))
    
    check_integration_files
    total_errors=$((total_errors + $?))
    
    check_python_dependencies
    total_errors=$((total_errors + $?))
    
    check_configuration
    total_errors=$((total_errors + $?))
    
    check_network
    total_errors=$((total_errors + $?))
    
    check_logs_and_disk
    total_errors=$((total_errors + $?))
    
    test_integration
    total_errors=$((total_errors + $?))
    
    # Summary
    if [ $total_errors -eq 0 ]; then
        log_message "INFO" "Health check completed successfully - All checks passed"
        exit 0
    else
        log_message "WARNING" "Health check completed with $total_errors issues"
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [--help] [--verbose]"
        echo ""
        echo "Wazuh MOPH Notify Integration Health Check"
        echo ""
        echo "Options:"
        echo "  --help, -h      Show this help message"
        echo "  --verbose, -v   Enable verbose output"
        echo ""
        echo "Log file: $LOG_FILE"
        exit 0
        ;;
    --verbose|-v)
        set -x
        ;;
esac

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Run main function
main "$@"