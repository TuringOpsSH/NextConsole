# Changelog

All notable changes to this project will be documented in this file.  
Format adheres to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2.9] - 2025-11-23

### New Features

- Workbench knowledge search supports adding from the Resource Library directory tree  
- Team members can upload, update, and delete shared resources in the Resource Library  
- Application Factory adds a variable transformation node for easy fixed-text composition and variable construction  
- Management console monitoring center adds user-level leaderboards 📈  
- Smart applications support third-party application integration via SDK  
- Smart applications can view publishing details  
- Supports parsing and processing of Think tags for privatized models  

### Fixes and Optimizations

- Fixed an issue with the first use of knowledge base Q&A in the Workbench  
- Fixed an issue with batch delivery of internal messages  
- Optimized user interaction and improved performance in the Application Factory



## [0.2.8] - 2025-10-31
 
### New Features
 
1. Enhanced knowledge Q&A node functionality (dynamic parameter passing, parallel processing, result deduplication, jump to upload resources)
2. Support for configuring workspace RAG search parameters
3. Workflows can be configured to start via forms
4. Support for editing user information and organization information in the user center
5. Support for user deletion
 
### Fixes & Optimizations
 
1. Fixed abnormal session auto-naming when the default model is an inference model
2. Optimized configuration data loading timing
3. Improved experience for workspace resource search and resource library search
4. Fixed abnormal direct resource upload interface
5. Optimized rendering of private inference model results
6. Fixed and improved the creation and management process of model instances
7. Fixed PDF parsing abnormalities
8. Optimized user center layout
9. Fixed abnormal search and add friend functionality
10. Optimized some front-end code standards
11. Fixed truncation issue with overly long custom messages
12. Optimized results in the inference area
13. Fixed issue where abnormal messages in test sessions were not fully rendered
14. Fixed abnormal issue with folder resource uploads
15. Fixed abnormal user token copying issue
16. Fixed incomplete execution result saving in start nodes
17. Fixed application authorization friend issue
18. Fixed abnormal batch notification in internal messages
19. Fixed reference exception issue for format-restricted file parameters in start nodes

## [0.2.7] - 2025-09-26

### Features

**Model Management Module Refactor**
  - [x] Refined model integration process
  - [x] Support for text generation, reasoning models, vector models, ranking models, and image understanding models
  - [x] Support for instant health testing
  - [x] Support for runtime parameter configuration
  - [x] Support for model permission management
  - [x] Support for viewing model runtime status

### Fixes and Improvements

- [x] Fixed format restrictions for file list parameters
- [x] Optimized the data model for model parameters
- [x] Added headers to Extra-body
- [x] After application publication, automatically add authorization to self by default
- [x] Optimized layout of AI Application Factory
- [x] Agent nodes can search and select models
- [x] Nodes can directly create duplicates
- [x] Added icons to backend management menu keys
- [x] Support for launching services from source code on Mac
- [x] Official assistants can modify names and icons
- [x] Introduced store in Application Factory
- [x] Fixed coding standards for some components


---

## [0.2.6] - 2025-09-09

### New Features

**Official Documentation Launch**
*   [x] Added User Center documentation
    *   Introduces product features and usage methods
    *   Company and team overview
    *   API specifications
    *   Technical blog

**User Center Expansion & Refactor**
*   [x] Refactored User Center interface, added a new Configuration Management module
    *   View API-key and expiration time, support extending expiration to a specified date
    *   View roles assigned to the current user
    *   Supports modifying the session layout mode for AI Workbench - XiaoYi Assistant
    *   Supports modifying the available model list for AI Workbench - XiaoYi Assistant
    *   Supports modifying the Auto-Build switch for AI Resource Library
    *   Supports modifying Contact configuration -- Allow being found by strangers
    *   Supports viewing the current version and checking for updates
*   [x] Added Platform Configuration page, supports modifying platform-level parameters
    *   Supports configuring the default model for XiaoYi Assistant
    *   Configure vectorization model address
    *   Configure re-ranking model address
    *   Configure speech recognition model address
    *   Configure WeChat login parameters
    *   Configure search engine parameters
    *   Configure mail server parameters
    *   Configure SMS service parameters
    *   Configure WPS service parameters (Enable to use WPS-related features for collaborative document editing)
    *   Supports custom branding (Logo modification, browser tab title, etc.)

**AI Workbench**
*   [x] File splitting now supports a list mode.

**Architectural Changes**
*   [x] Changed routing mode to history mode, removing the `#` from URLs
*   [x] Introduced ESLint for unified code style enforcement
*   [x] Introduced Pinia for state management

### Fixes & Optimizations

**AI Workbench**
*   [x] Fixed abnormal display of answers after manually interrupting XiaoYi Assistant
*   [x] Fixed message copy functionality
*   [x] Fixed input box enter key event handling
*   [x] Fixed session parameters automatically closing
*   [x] Fixed abnormal menu highlighting

**Reports**
*   [x] Optimized report interface and loading performance

**AI App Factory**
*   [x] Limited RAG length to prevent overflow issues
*   [x] Fixed trace log overwrite anomaly

---

## [0.2.5] - 2025-08-24

### Fixes

- [x] Optimized runtime logs for agent nodes  
- [x] Fixed Excel parsing exceptions  
- [x] Fixed text parsing exceptions  
- [x] Fixed PDF-to-PNG conversion failures  
- [x] Fixed rendering for custom message formats  
- [x] Replaced image recognition format with base64 in concurrent agent mode  
- [x] Fixed DOCX icon display  
- [x] Fixed boolean parameter passing exceptions  
- [x] Fixed real-time error streaming notifications  
- [x] Fixed file-list parameter upload and switching issues  
- [x] Fixed table styling abnormalities  
- [x] Fixed inference area rendering styles  
- [x] Fixed code block line numbering  
- [x] Adjusted AI workbench panel height  
- [x] Fixed keyboard file copy exception during XiaoYi assistant session initialization  
- [x] Optimized shared resource styling  
- [x] Improved slow response for batch user imports  
- [x] Fixed enterprise admin user import exceptions  
- [x] Fixed browser caching issues in management console  
 

## [0.2.4] - 2025-08-10

### Added
- [x] Support for defining session parameters on the start node.
- [x] Support for file reading nodes.
- [x] Support for text segmentation nodes.
- [x] Support for sub - workflow nodes.
- [x] Parameter definition and passing support multi - selection and required fields.
- [x] Support for managing resource parsing results and segmentation results in the resource library, and conducting segmentation similarity tests.

### Fixed
- Optimized the ratio of UI elements to fit laptop screens.
- Fixed the abnormal calculation of recall similarity.
- Fixed the abnormal capture during the rerank process.
- Handled the exceptions in parameter definition and passing.
- Fixed the abnormal order of agent application.
- Fixed the abnormal parsing of pandoc.
- Fixed some known bugs.

## [0.1.0] - 2025-07-24
### Changed
- Enhanced repository metadata (README/CONTRIBUTING)
- Added Docker deployment image

## [0.0.1] - 2025-07-22
### Added
- Project repository initialized
- Core code framework committed