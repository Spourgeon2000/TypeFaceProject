package com.project.sdk.fileuploadingsystem.configurations.service;


import com.project.sdk.fileuploadingsystem.configurations.data.File;
import com.project.sdk.fileuploadingsystem.configurations.repository.FileUploadRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.gridfs.GridFsTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Service
@Slf4j
public class FileService {

    private static final String UPLOAD_DIR = "uploads/";

    private final FileUploadRepository fileUploadRepository;

    private final GridFsTemplate gridFsTemplate;

    public FileService(FileUploadRepository fileUploadRepository, GridFsTemplate gridFsTemplate) {
        this.fileUploadRepository = fileUploadRepository;
        this.gridFsTemplate = gridFsTemplate;
    }

    public File uploadFile(MultipartFile file, String userId) throws IOException {
        // Generate a unique file name and save the file to disk
        String fileName = System.currentTimeMillis() + "_" + file.getOriginalFilename();
        String fileId = gridFsTemplate.store(file.getInputStream(), fileName, file.getContentType()).toString();

        // Save the metadata to the MongoDB collection
        File fileUpload = new File();
        fileUpload.setUserId(userId);
        fileUpload.setFileName(file.getOriginalFilename());
        fileUpload.setFileType(file.getContentType());
        fileUpload.setFileSize(file.getSize());
        fileUpload.setUploadedTimeStamp(new java.util.Date());
        fileUpload.setFileId(fileId);

        return fileUploadRepository.save(fileUpload);
    }


    public Optional<File> getFileMetadata(String fileId) {
        return fileUploadRepository.findById(fileId);
    }


    // Get all files
    public List<File> getAllFiles() {
        return fileUploadRepository.findAll();
    }

    // List all uploaded files in some local file if not mongo dv
    public List<String> loadAllFiles() {
        try (Stream<Path> paths = Files.walk(Paths.get(UPLOAD_DIR))) {
            return paths.filter(Files::isRegularFile)
                    .map(path -> path.getFileName().toString())
                    .collect(Collectors.toList());
        } catch (IOException e) {
            throw new RuntimeException("Could not list files", e);
        }
    }
}
