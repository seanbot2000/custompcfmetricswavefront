package com.vmware.custompcfmetrics.modules;

import org.cloudfoundry.client.lib.CloudFoundryClient;
import org.cloudfoundry.client.lib.domain.CloudSpace;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import com.vmware.custompcfmetrics.Metric;

@Component
public class SpacesModule extends CustomPCFMetricsBaseModule implements CustomPcfMetricsModule {
    
    private static final Logger log = LoggerFactory.getLogger(SpacesModule.class);
    private static final CloudFoundryClient client = null;

    @Scheduled(fixedRate = 5000)
    public processMetrics(){
        client = getClient();
        ArrayList<String> ccResponse = callCCAPI(client);
        ArrayList<Metric> customMetrics = createCustomMetrics(ccResponse);
        sendCustomMetrics(ArrayList<Metric>);
    }

	public ArrayList<String> callCCAPI(CloudFoundryClient client){
        ArrayList<String> spaces = new ArrayList<String>();
		for (CloudSpace space : client.getSpaces()) {
            log.info("  %s\t(%s)%n", space.getName(), space.getOrganization().getName());
            spaces.add("  %s\t(%s)%n", space.getName(), space.getOrganization().getName())
        }
        return spaces;
	}

    ArrayList<Metric> createCustomMetrics(ArrayList<String> ccResponse){
        ArrayList<Metric> metrics = new ArrayList<Metric>();
        
    }
}
