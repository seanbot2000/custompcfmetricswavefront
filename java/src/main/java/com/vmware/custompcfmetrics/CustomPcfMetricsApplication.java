package com.vmware.custompcfmetricswavefront;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@EnableScheduling
public class PcfMetricsApplication {

	private static final Logger log = LoggerFactory.getLogger(PcfMetricsApplication.class);

	public static void main(String[] args) {
		SpringApplication.run(PcfMetricsApplication.class, args);
	}

}
