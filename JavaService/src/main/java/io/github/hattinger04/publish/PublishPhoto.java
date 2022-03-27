package io.github.hattinger04.publish;
import java.io.IOException;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import io.github.hattinger04.PropertiesConfig;
/**
 * 
 * @author Hattinger04
 *
 */

public class PublishPhoto {

	private static String username;
	private static String password;
	private static String broker;
	private static String channel;
	private final static String clientId = "JavaServicePublishPhoto";

	private static PropertiesConfig propertiesConfig; 

	
	public static void main(String[] args) throws IOException {
		propertiesConfig = new PropertiesConfig(); 
		propertiesConfig.loadProperties();
		MemoryPersistence persistence = new MemoryPersistence();

		username = propertiesConfig.getProperty("username"); 
		password = propertiesConfig.getProperty("password"); 
		broker = String.format("tcp://%s:%s", propertiesConfig.getProperty("host"), propertiesConfig.getProperty("port"));
		channel = propertiesConfig.getProperty("channelPublish"); 

		String content = "photo"; 
		int qos = 2; 
		
		try {
			MqttClient client = new MqttClient(broker, clientId, persistence);
			MqttConnectOptions connOpts = new MqttConnectOptions();
			connOpts.setCleanSession(true);
			connOpts.setUserName(username);
			connOpts.setPassword(password.toCharArray());

			System.out.println("Connecting to broker: " + broker);
			client.connect(connOpts);
			System.out.println("Connected");

			System.out.println("Publishing message: " + content);
			MqttMessage message = new MqttMessage(content.getBytes());
			message.setQos(qos);
			client.publish(channel, message);
			client.disconnect();
			System.out.println("Disconnected");
			System.exit(0);
		} catch (MqttException me) {
			me.printStackTrace();
		}
	}
}
