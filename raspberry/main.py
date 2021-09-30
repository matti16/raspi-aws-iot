import click
import time

from raspi_aws_iot.mqtt import MQTTConnection
from raspi_aws_iot.config import MQTTConfig, DeviceConfig
from raspi_aws_iot.controller import Controller

ctrl = Controller(DeviceConfig.LEDS)


def on_msg_received(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received message from topic '{topic}': {payload}")
    try:
        ctrl.parse_msg(payload)
    except Exception as e:
        print(e)


@click.command()
@click.option('--endpoint', default=MQTTConfig.ENDPOINT, help="Your AWS IoT custom endpoint, not including a port.")
@click.option('--port', type=int, default=MQTTConfig.PORT, help="Specify port. AWS IoT supports 443 and 8883.")
@click.option('--cert', default=MQTTConfig.CERT, help="File path to your client certificate, in PEM format.")
@click.option('--key', default=MQTTConfig.KEY, help="File path to your private key, in PEM format.")
@click.option('--root-ca', default=MQTTConfig.ROOT_CA, help="File path to root certificate authority, in PEM format. " +
                                      "Necessary if MQTT server uses a certificate that's not already in " +
                                      "your trust store.")
@click.option('--client-id', default=MQTTConfig.CLIENT_ID, help="Client ID for MQTT connection.")
@click.option('--topic', default=MQTTConfig.TOPIC, help="Topic to subscribe to, and publish messages to.")
def cmd_line_main(endpoint, port, cert, key, root_ca, client_id, topic):
    mqtt_connection = MQTTConnection(endpoint, port, cert, key, root_ca, client_id)
    mqtt_connection.connect()
    mqtt_connection.subscribe(topic, on_msg_received)

    while True:
        try:
            time.sleep(10)
        except Exception as e:
            print(e)
            mqtt_connection.disconnect()
            break

if __name__ == '__main__':
    cmd_line_main()