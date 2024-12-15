package com.project.sdk.fileuploadingsystem.configurations.launcher;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.SimpleMongoClientDatabaseFactory;
import org.springframework.data.mongodb.gridfs.GridFsTemplate;

@Configuration
public class MongoConfig {

    @Bean
    public MongoTemplate mongoTemplate() throws Exception {
        return new MongoTemplate(new SimpleMongoClientDatabaseFactory("mongodb://localhost:27017/uploads"));
    }

    @Bean
    public GridFsTemplate gridFsTemplate(MongoTemplate mongoTemplate) throws Exception {
        return new GridFsTemplate(mongoTemplate.getMongoDbFactory(), mongoTemplate.getConverter());
    }
}
