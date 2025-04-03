# Introduction

FromEdwin is a monitoring platform for web-related projects. It is a highly opinionated system that aims to provide comprehensive monitoring services with minimal configuration required from users.

For each project to monitor, providing its url will trigger a list of automated script:
- fetch favicon
- load sitemap.xml
- measure availability and alert any outrage
- For each URL in sitemaps app will measure :
  - the performance using lighthouse
  - show title, description, and key words
