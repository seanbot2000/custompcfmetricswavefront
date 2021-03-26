package com.vmware.custompcfmetricswavefront;

public class Metric{

    private String name;
    private double value;
    private Long timestamp;
    private String source;
    private Map<String, String> tags;

    public Metric() {}

    public String getName(){
        return name;
    }

    public void setName(String name)
    {
        this.name = name;
    }

    public double getValue()
    {
        return value;
    }

    public void setValue(double value)
    {
        this.value = value;
    }

    public Long getTimestamp()
    {
        return timestamp;
    }

    public void setTimestamp(Long timestamp)
    {
        this.timestamp = timestamp;
    }

    public String getSource()
    {
        return source;
    }

    public void setSource(String source)
    {
        this.source = source;
    }

    public Map<String, String> getTags()
    {
        return tags;
    }

    public void setTags(Map<String, String> tags)
    {
        this.tags = tags;
    }

}