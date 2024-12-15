package com.project.sdk.fileuploadingsystem.configurations.repository;


import com.project.sdk.fileuploadingsystem.configurations.data.File;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface FileUploadRepository extends MongoRepository<File, String> {
}