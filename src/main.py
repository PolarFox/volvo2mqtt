import logging
from volvo import authorize
from mqtt import update_loop, connect, request_otp
from const import VERSION
from util import set_tz, setup_logging, set_mqtt_settings, validate_settings
import sys
import time


if __name__ == '__main__':
    try:
        setup_logging()
        logging.info("Starting volvo2mqtt version " + VERSION)
        validate_settings()
        set_tz()
        set_mqtt_settings()
        
        # First connect to MQTT - needed for both normal auth and OTP flow
        connect()
        
        while True:
            try:
                # Try to authorize with Volvo
                authorize()
                # If authorization succeeds, start the update loop
                update_loop()
                # If update_loop exits, we'll try to reauthorize
            except Exception as e:
                if "OTP authentication required" in str(e):
                    # For OTP, we're already connected to MQTT and entities are created
                    # Just log and wait for user to handle OTP via MQTT command
                    logging.info(str(e))
                    # Wait until user requests OTP via MQTT
                    while not request_otp:
                        time.sleep(1)
                    continue
                else:
                    # For other auth errors, log and exit
                    logging.error(f"Authorization failed: {str(e)}")
                    sys.exit(1)
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)
