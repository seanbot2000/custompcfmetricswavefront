package com.vmware.custompcfmetrics.modules;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.cloudfoundry.client.lib.CloudCredentials;
import org.cloudfoundry.client.lib.CloudFoundryClient;

import com.vmware.custompcfmetrics.Metric;

public class PcfMetricsBaseModule {
    
    @Value("${ccapi.user}")
    private String ccapiUser;

    @Value("${ccapi.password}")
    private String ccapiPassword;

    @Value("${ccapi.target}")
    private String ccapiTarget;

    @Value("${wavefront.endpoint}")
    private String wavefrontEndpoint;

    @Value("${wavefront.token}")
    private String wavefrontToken;

    private static final Logger log = LoggerFactory.getLogger(PcfMetricsBaseModule.class);
    private WavefrontSender sender = null;

    protected static CloudFoundryClient getClient(){
        CloudCredentials credentials = new CloudCredentials(ccapiUser, ccapiPassword);
        CloudFoundryClient client = new CloudFoundryClient(credentials, getTargetURL(ccapiTarget));
        client.login();
        return client;
    }
    
    protected static void sendCustomMetric(ArrayList<Metric> metrics){
        WavefrontClientFactory wavefrontClientFactory = new WavefrontClientFactory();
        wavefrontClientFactory.addClient(getWavefrontUrl(), 20000, 100000, 2, Integer.MAX_VALUE);
        sender = wavefrontClientFactory.getClient();

        for(Metric metric: metrics)
        {
            sender.sendMetric(metric.getName(), metric.getValue(), metric.getTimestamp(), metric.getSource(), metric.getTags());
        }

        int totalFailures = wavefrontSender.getFailureCount();
        log.info("Total Failures sending custom metrics: %i", totalFailures);

        sender.flush();
        sender.close();
    }

    protected static String getWavefrontUrl()
    {
        StringBuilder url = new StringBuilder();
        url.append("https://");
        url.append(wavefrontToken);
        url.append("@");
        url.append(wavefrontEndpoint);

        return url.toString();
    }
}