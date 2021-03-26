package com.vmware.custompcfmetrics.interfaces;

import org.cloudfoundry.client.lib.CloudFoundryClient;
import com.vmware.custompcfmetrics.Metric;

public interface CustomPcfMetricsModule {
    ArrayList<String> callCCAPI(CloudFoundryClient client);
    ArrayList<Metric> createCustomMetrics(ArrayList<String>);
}
