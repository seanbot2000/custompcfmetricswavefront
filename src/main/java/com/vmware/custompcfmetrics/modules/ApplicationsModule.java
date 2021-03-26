package com.vmware.custompcfmetrics.modules;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
@Scheduled
public class ApplicationsModule extends CustomPCFMetricsBaseModule implements CustomPcfMetricsModule{
    
    private static final Logger log = LoggerFactory.getLogger(ApplicationsModule.class);

    @Scheduled(fixedRate = 5000)
    public String callCCAPI(String endpoint){

    }
}
