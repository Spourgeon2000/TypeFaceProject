package com.project.sdk.fileuploadingsystem.configurations.controller;

import com.mongodb.client.gridfs.model.GridFSFile;
import com.project.sdk.fileuploadingsystem.configurations.data.File;
import com.project.sdk.fileuploadingsystem.configurations.service.FileService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.gridfs.GridFsTemplate;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.Optional;


@RequestMapping("/file")
@RestController
@Slf4j
public class FileController {

    private final FileService fileService;

    private final GridFsTemplate gridFsTemplate;

    @Autowired
    public FileController(FileService fileService, GridFsTemplate gridFsTemplate) {
        this.fileService = fileService;
        this.gridFsTemplate = gridFsTemplate;
    }

    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file,
                                             @RequestParam("userId") String userId) {
        if (file.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("No file uploaded");
        }
        try {
            File uploadFile = fileService.uploadFile(file, userId);
            return ResponseEntity.ok("File uploaded successfully. File ID: " + uploadFile.getId());
        } catch (IOException e) {
            return ResponseEntity.status(500).body("Error uploading file: " + e.getMessage());
        }
    }

    // Get file by ID for downloading
    @GetMapping("/{id}")
    public ResponseEntity<Resource> getFile(@PathVariable String id) {
        Optional<File> fileMetadataOptional = fileService.getFileMetadata(id);  // Get metadata from DB
        GridFSFile gridFSFile = gridFsTemplate.findOne(Query.query(Criteria.where("_id").is(fileMetadataOptional.get().getFileId())));
        HttpHeaders headers = new HttpHeaders();
        Resource resource;
        try {
            resource = gridFsTemplate.getResource(gridFSFile);
            headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + gridFSFile.getFilename() + "\"");
            headers.add(HttpHeaders.CONTENT_TYPE, gridFSFile.getMetadata().get("_contentType").toString());
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
        // Return the file as a downloadable resource
        return ResponseEntity.ok()
                .headers(headers)
                .body(resource);

    }

    // Get a list of all files
    @GetMapping("/")
    public ResponseEntity<List<File>> getAllFiles() {
        List<File> files = fileService.getAllFiles();
        return ResponseEntity.ok(files);
    }
}
