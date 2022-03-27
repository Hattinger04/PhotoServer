package io.github.hattinger04;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;

import lombok.Getter;

/**
 * 
 * @author Hattinger04
 *
 */
public class PropertiesConfig {

	private Properties prop;
	@Getter
	private final File file;
	private final boolean createProperties = false;

	public PropertiesConfig() throws IOException {
		file = new File("src/main/resources/keys.txt");
		init();
	}

	public static void main(String[] args) throws IOException {
		PropertiesConfig con = new PropertiesConfig();
		con.init();
	}

	private void init() throws IOException {
		prop = new Properties();
		if (createProperties) {
			createDefaultProperties();
		}
	}

	public void saveProperties(Properties p) throws IOException {
		FileOutputStream fileOutputStream = new FileOutputStream(file);
		prop.store(fileOutputStream, "Properties");
		fileOutputStream.close();
	}

	public void loadProperties() throws IOException {
		FileInputStream fileInputStream = new FileInputStream(file);
		prop.load(fileInputStream);
		fileInputStream.close();
	}

	public void setProperty(String key, String value) throws IOException {
		loadProperties();
		prop.setProperty(key, value);
		saveProperties(prop);
	}

	public String getProperty(String key) {
		return prop.getProperty(key);
	}

	private void createDefaultProperties() throws IOException {
		setProperty("username", "");
		setProperty("password", "");
		setProperty("host", "");
		setProperty("port", "");
		setProperty("channelSubscribe", "");
		setProperty("channelPublish", "");
		setProperty("countPictures", "0");
	}
}
