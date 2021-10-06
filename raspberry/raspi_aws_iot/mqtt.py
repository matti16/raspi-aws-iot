from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))
    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            raise Exception("Server rejected resubscribe to topic: {}".format(topic))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))
    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()
        resubscribe_future.add_done_callback(on_resubscribe_complete)


class MQTTConnection:

    def __init__(
        self,
        endpoint,
        port,
        cert_filepath,
        pri_key_filepath,
        ca_filepath,
        client_id,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=None,
    ):

        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=endpoint,
            port=port,
            cert_filepath=cert_filepath,
            pri_key_filepath=pri_key_filepath,
            client_bootstrap=client_bootstrap,
            ca_filepath=ca_filepath,
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=client_id,
            clean_session=clean_session,
            keep_alive_secs=keep_alive_secs,
            http_proxy_options=http_proxy_options,
        )
    
    def connect(self):
        connect_future = self.mqtt_connection.connect()
        connect_future.result()
        print("Connected!")

    def subscribe(self, topic, callback, qos=mqtt.QoS.AT_LEAST_ONCE):
        subscribe_future, _ = self.mqtt_connection.subscribe(
            topic=topic,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=callback
        )
        subscribe_result = subscribe_future.result()
        print(f"Subscribed to {topic} with {subscribe_result['qos']}")
    
    def disconnect(self):
        print("Disconnecting...")
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")
    
    def send_message(self, topic, message):
        self.mqtt_connection.publish(
            topic=topic,
            payload=message,
            qos=mqtt.QoS.AT_LEAST_ONCE)
        print(f"Sent message to {topic}")

    


