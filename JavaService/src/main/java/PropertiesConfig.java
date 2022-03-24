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
	
	public PropertiesConfig() {
        file = new File("src/main/resources/keys.txt"); 
		init(); 
	}
	
	public static void main(String[] args) {
		PropertiesConfig con = new PropertiesConfig(); 
		con.init();
		
	}
	
	private void init() {
        prop = new Properties(); 
        if(createProperties) {
        	createDefaultProperties();
        }
	}
	
	public void saveProperties(Properties p) throws IOException{
		FileOutputStream fileOutputStream = new FileOutputStream(file); 
		prop.store(fileOutputStream, "Properties");
		fileOutputStream.close();
	}
	
	public void loadProperties() throws IOException {
		FileInputStream fileInputStream = new FileInputStream(file); 
		prop.load(fileInputStream);
		fileInputStream.close();
	}
	
	public void setProperty(String key, String value) {
		prop.setProperty(key, value); 
	}
	
	public String getProperty(String key) {
		return prop.getProperty(key); 
	}
	
	private void createDefaultProperties() {
        setProperty("username", "");
        setProperty("password", "");
        setProperty("host", "");
        setProperty("port", "");
        setProperty("channelSubscribe", "");
        setProperty("channelPublish", "");

        try {
			saveProperties(prop);
		} catch (IOException e) {
			e.printStackTrace();
		}

	}
}
