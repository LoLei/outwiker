﻿<?xml version="1.0" encoding="utf-8"?>
<!-- Read this before creating packages: https://chocolatey.org/docs/create-packages -->
<!-- It is especially important to read the above link to understand additional requirements when publishing packages to the community feed aka dot org (https://chocolatey.org/packages). -->

<!-- Test your packages in a test environment: https://github.com/chocolatey/chocolatey-test-environment -->

<!--
This is a nuspec. It mostly adheres to https://docs.nuget.org/create/Nuspec-Reference. Chocolatey uses a special version of NuGet.Core that allows us to do more than was initially possible. As such there are certain things to be aware of:

* the package xmlns schema url may cause issues with nuget.exe
* Any of the following elements can ONLY be used by choco tools - projectSourceUrl, docsUrl, mailingListUrl, bugTrackerUrl, packageSourceUrl, provides, conflicts, replaces 
* nuget.exe can still install packages with those elements but they are ignored. Any authoring tools or commands will error on those elements 
-->

<!-- You can embed software files directly into packages, as long as you are not bound by distribution rights. -->
<!-- * If you are an organization making private packages, you probably have no issues here -->
<!-- * If you are releasing to the community feed, you need to consider distribution rights. -->
<!-- Do not remove this test for UTF-8: if “Ω” doesn’t appear as greek uppercase omega letter enclosed in quotation marks, you should use an editor that supports UTF-8, not this one. -->
<package xmlns="http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd">
  <metadata>
    <!-- == PACKAGE SPECIFIC SECTION == -->
    <!-- This section is about this package, although id and version have ties back to the software -->
    <!-- id is lowercase and if you want a good separator for words, use '-', not '.'. Dots are only acceptable as suffixes for certain types of packages, e.g. .install, .portable, .extension, .template -->
    <!-- If the software is cross-platform, attempt to use the same id as the debian/rpm package(s) if possible. -->
    <id>outwiker-unstable</id>
    <!-- version should MATCH as closely as possible with the underlying software -->
    <!-- Is the version a prerelease of a version? https://docs.nuget.org/create/versioning#creating-prerelease-packages -->
    <!-- Note that unstable versions like 0.0.1 can be considered a released version, but it's possible that one can release a 0.0.1-beta before you release a 0.0.1 version. If the version number is final, that is considered a released version and not a prerelease. -->
    <version>$version</version>
    <!-- <packageSourceUrl>Where is this Chocolatey package located (think GitHub)? packageSourceUrl is highly recommended for the community feed</packageSourceUrl>-->
    <!-- owners is a poor name for maintainers of the package. It sticks around by this name for compatibility reasons. It basically means you. -->
    <!--<owners>__REPLACE_YOUR_NAME__</owners>-->
    <!-- ============================== -->

    <!-- == SOFTWARE SPECIFIC SECTION == -->
    <!-- This section is about the software itself -->
    <title>outwiker (Install)</title>
    <authors>Eugene Ilin</authors>
    <!-- projectUrl is required for the community feed -->
	<projectUrl>https://jenyay.net/OutwikerEn</projectUrl>
    <!--<iconUrl>http://cdn.rawgit.com/__REPLACE_YOUR_REPO__/master/icons/outwiker.png</iconUrl>-->
    <!-- <copyright>Year Software Vendor</copyright> -->
    <!-- If there is a license Url available, it is required for the community feed -->
    <!-- <licenseUrl>Software License Location __REMOVE_OR_FILL_OUT__</licenseUrl>
    <requireLicenseAcceptance>true</requireLicenseAcceptance>-->
    <!--<projectSourceUrl>Software Source Location - is the software FOSS somewhere? Link to it with this</projectSourceUrl>-->
    <!--<docsUrl>At what url are the software docs located?</docsUrl>-->
    <!--<mailingListUrl></mailingListUrl>-->
    <!--<bugTrackerUrl></bugTrackerUrl>-->
    <tags>outwiker outliner notes notepad tree</tags>
    <summary>OutWiker is designed to store notes in a tree</summary>
    <description>OutWiker is designed to store notes in a tree. Such programs are called "outliner", personal wiki, or tree-like editors. OutWiker's main difference from the other similar programs is keeping the tree of notes in the form of directories on disk, and encouraging changing the base by external sources and programs.

Also any number of files can be attached to the page. OutWiker can contain pages of different types, currently supports three types of pages: plain text, HTML pages and wiki pages, but the number of types of pages will increase in future. </description>
    <!-- <releaseNotes>__REPLACE_OR_REMOVE__MarkDown_Okay</releaseNotes> -->
    <!-- =============================== -->      

    <!-- Specifying dependencies and version ranges? https://docs.nuget.org/create/versioning#specifying-version-ranges-in-.nuspec-files -->
    <!--<dependencies>
      <dependency id="" version="__MINIMUM_VERSION__" />
      <dependency id="" version="[__EXACT_VERSION__]" />
      <dependency id="" version="[_MIN_VERSION_INCLUSIVE, MAX_VERSION_INCLUSIVE]" />
      <dependency id="" version="[_MIN_VERSION_INCLUSIVE, MAX_VERSION_EXCLUSIVE)" />
      <dependency id="" />
      <dependency id="chocolatey-core.extension" version="1.1.0" />
    </dependencies>-->
    <!-- chocolatey-core.extension - https://chocolatey.org/packages/chocolatey-core.extension
         - You want to use Get-UninstallRegistryKey on less than 0.9.10 (in chocolateyUninstall.ps1)
         - You want to use Get-PackageParameters and on less than 0.11.0
         - You want to take advantage of other functions in the core community maintainer's team extension package
    -->

    <!--<provides>NOT YET IMPLEMENTED</provides>-->
    <!--<conflicts>NOT YET IMPLEMENTED</conflicts>-->
    <!--<replaces>NOT YET IMPLEMENTED</replaces>-->
  </metadata>
  <files>
    <!-- this section controls what actually gets packaged into the Chocolatey package -->
    <file src="tools\**" target="tools" />
    <!--Building from Linux? You may need this instead: <file src="tools/**" target="tools" />-->
  </files>
</package>
