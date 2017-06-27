CREATE TABLE `cmdb_app_host` (
  `app_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  `app_version` varchar(64) DEFAULT NULL,
  KEY `app_id` (`app_id`),
  KEY `host_id` (`host_id`)
) ENGINE=innodb DEFAULT CHARSET=utf8 ;




 CREATE TABLE `cmdb_application` (
  `app_id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(64) DEFAULT NULL,
  `app_note` varchar(64) DEFAULT NULL,
  `app_type` varchar(64) DEFAULT NULL,
  `app_version` varchar(64) DEFAULT NULL,
  `app_user` varchar(64) DEFAULT NULL,
  `app_product` int(11) DEFAULT NULL,
  PRIMARY KEY (`app_id`),
  KEY `app_product` (`app_product`)
) ENGINE=innodb AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 ;



CREATE TABLE `cmdb_asset` (
  `host_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_hostname` varchar(50) DEFAULT NULL,
  `system_ip` varchar(256) DEFAULT NULL,
  `device_type` varchar(64) DEFAULT NULL,
  `device_model` varchar(64) DEFAULT NULL,
  `father_id` varchar(64) DEFAULT NULL,
  `system_network_card` varchar(164) DEFAULT NULL,
  `system_user` varchar(256) DEFAULT NULL,
  `system_userpass` varchar(256) DEFAULT NULL,
  `idc_id` varchar(50) DEFAULT NULL,
  `system_note` varchar(256) DEFAULT NULL,
  `system_kernel` varchar(256) DEFAULT NULL,
  `system_version` varchar(256) DEFAULT NULL,
  `system_mac` varchar(256) DEFAULT NULL,
  `physical_memory` varchar(64) DEFAULT NULL,
  `system_swap` varchar(64) DEFAULT NULL,
  `memory_slots_number` varchar(30) DEFAULT NULL,
  `logical_cpu_cores` varchar(64) DEFAULT NULL,
  `physical_cpu_cores` varchar(64) DEFAULT NULL,
  `physical_cpu_model` varchar(64) DEFAULT NULL,
  `hard_disk` varchar(64) DEFAULT NULL,
  `ethernet_interface` varchar(1000) DEFAULT NULL,
  `device_Sn` varchar(164) DEFAULT NULL,
  `idrac_ip` varchar(256) DEFAULT NULL,
  `idrac_user` varchar(256) DEFAULT NULL,
  `idrac_userpass` varchar(256) DEFAULT NULL,
  `group_id` varchar(256) DEFAULT NULL,
  `system_status` varchar(64) DEFAULT NULL,
  `idc_cabinet` varchar(64) DEFAULT NULL,
  `idc_un` varchar(64) DEFAULT NULL,
  `models` varchar(64) DEFAULT NULL,
  `father_ip` varchar(64) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `guarantee_date` varchar(100) DEFAULT NULL,
  `application_server` varchar(64) DEFAULT NULL,
  `application_status` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`host_id`)
) ENGINE=innodb AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 ;





CREATE TABLE `cmdb_asset_offline` (
  `host_id` int(11) NOT NULL AUTO_INCREMENT,
  `system_hostname` varchar(50) DEFAULT NULL,
  `system_ip` varchar(256) DEFAULT NULL,
  `device_type` varchar(64) DEFAULT NULL,
  `device_model` varchar(64) DEFAULT NULL,
  `father_id` varchar(64) DEFAULT NULL,
  `system_network_Card` varchar(164) DEFAULT NULL,
  `system_user` varchar(256) DEFAULT NULL,
  `system_userpass` varchar(256) DEFAULT NULL,
  `idc_id` varchar(50) DEFAULT NULL,
  `system_note` varchar(256) DEFAULT NULL,
  `system_kernel` varchar(256) DEFAULT NULL,
  `system_version` varchar(256) DEFAULT NULL,
  `system_mac` varchar(256) DEFAULT NULL,
  `physical_memory` varchar(64) DEFAULT NULL,
  `system_swap` varchar(64) DEFAULT NULL,
  `memory_slots_number` varchar(30) DEFAULT NULL,
  `logical_cpu_cores` varchar(64) DEFAULT NULL,
  `physical_cpu_cores` varchar(64) DEFAULT NULL,
  `physical_cpu_model` varchar(64) DEFAULT NULL,
  `hard_disk` varchar(64) DEFAULT NULL,
  `ethernet_interface` varchar(1000) DEFAULT NULL,
  `device_Sn` varchar(164) DEFAULT NULL,
  `idrac_ip` varchar(256) DEFAULT NULL,
  `idrac_user` varchar(256) DEFAULT NULL,
  `idrac_userpass` varchar(256) DEFAULT NULL,
  `group_id` varchar(256) DEFAULT NULL,
  `system_status` varchar(64) DEFAULT NULL,
  `idc_cabinet` varchar(64) DEFAULT NULL,
  `idc_un` varchar(64) DEFAULT NULL,
  `models` varchar(64) DEFAULT NULL,
  `father_ip` varchar(64) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `guarantee_date` varchar(100) DEFAULT NULL,
  `offline_time` datetime DEFAULT NULL,
  `product_name` varchar(64) DEFAULT NULL,
  `appname_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`host_id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;



CREATE TABLE `cmdb_idc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `contact` varchar(30) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=innodb AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 ;



CREATE TABLE `cmdb_product` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(64) DEFAULT NULL,
  `product_user` varchar(64) DEFAULT NULL,
  `product_note` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=innodb AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 ;



CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`)
) ENGINE=innodb DEFAULT CHARSET=utf8 ;