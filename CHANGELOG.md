# Changelog

All notable changes to this project will be documented in this file.  
Format adheres to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


Here's the English version of the changelog with professional formatting:

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