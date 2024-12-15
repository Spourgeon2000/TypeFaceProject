package com.project.sdk.fileuploadingsystem.configurations.launcher;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@SpringBootApplication
@ComponentScan(
        basePackages = {"com.project"})
@EnableMongoRepositories(basePackages = "com.project.sdk.fileuploadingsystem.configurations.repository")
public class FileUploadingSystemLauncher {

    public static void main(String[] args) {
        // Launch the Spring Boot application
        SpringApplication.run(FileUploadingSystemLauncher.class, args);
    }
}