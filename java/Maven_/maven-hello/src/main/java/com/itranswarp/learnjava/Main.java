package com.itranswarp.learnjava;

import org.slf4j.LoggerFactory;

/**
 * App entry for Maven project.
 * 
 * @author liaoxuefeng
 */
public class Main {

	public static void main(String[] args) throws Exception {
		var logger = LoggerFactory.getLogger(Main.class);
		logger.info("start application...");
		for (int i = 1; i <= 10; i++) {
			Thread.sleep(100);
			logger.warn("begin task {}...", i);
		}
		logger.info("done.");
	}
}
