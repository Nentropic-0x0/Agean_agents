CREATE TABLE agent_metadata (
    uuid UUID PRIMARY KEY,                -- Universally unique identifier for the agent
    agent_type VARCHAR(255),              -- Type of agent (e.g., RLAgent, ThreatDetectionAgent)
    timestamp TIMESTAMP WITH TIME ZONE,   -- Timestamp of the message/event
    from_agent UUID,                      -- UUID of the agent sending the message
    to_agent UUID,                        -- UUID of the agent receiving the message
    message_id UUID,                      -- A unique ID for tracking individual messages between agents
    message JSONB                        -- Message JSON data sent between agents
);

CREATE TABLE ecs_cybersecurity (
    ecs_version VARCHAR(10) DEFAULT '1.12',  -- ECS version for compatibility
    event_id UUID PRIMARY KEY,               -- Unique ID for the event
    event_category VARCHAR(255),             -- Event category (e.g., intrusion, vulnerability, access)
    event_type VARCHAR(255),                 -- Type of event (e.g., alert, signal, detection)
    event_outcome VARCHAR(50),               -- Outcome of the event (e.g., success, failure)
    event_action VARCHAR(255),               -- Action taken (e.g., block, allow, escalate)
    source_ip INET,                          -- Source IP address
    destination_ip INET,                     -- Destination IP address
    user_id UUID,                            -- UUID of the user (if applicable)
    process_id INTEGER,                      -- Process ID related to the event
    file_path TEXT,                          -- Path of the file involved in the event (if applicable)
    threat_level VARCHAR(50),                -- Severity of the threat (e.g., low, medium, high)
    timestamp TIMESTAMP WITH TIME ZONE       -- Time the event was generated
);

-- Table for storing the messages exchanged between agents
CREATE TABLE agent_messages (
    message_id UUID PRIMARY KEY,          -- Unique message ID
    from_agent UUID,                      -- UUID of the agent sending the message
    to_agent UUID,                        -- UUID of the agent receiving the message
    timestamp TIMESTAMP WITH TIME ZONE,   -- Timestamp of the message
    message_type VARCHAR(50),             -- Instruction or response
    payload JSONB,                        -- Task instructions or data
    response JSONB,                       -- Response from the receiving agent
    FOREIGN KEY (from_agent) REFERENCES agent_metadata(uuid),
    FOREIGN KEY (to_agent) REFERENCES agent_metadata(uuid)
);

-- Indexing for faster search and retrieval of messages
CREATE INDEX idx_agent_timestamp ON agent_messages (from_agent, timestamp);

CREATE TABLE intelligence_reports (
    report_id UUID PRIMARY KEY,              -- Unique identifier for the intelligence report
    event_id UUID REFERENCES ecs_cybersecurity(event_id), -- Link to ECS event table
    report_generated_at TIMESTAMP WITH TIME ZONE, -- Timestamp when the report was generated
    report_author VARCHAR(255),              -- Author or system that generated the report

    -- Base Fields (directly captured or provided data)
    threat_actor VARCHAR(255),               -- Identified threat actor (if any)
    malware_family VARCHAR(255),             -- Type or family of malware involved (if applicable)
    target_sector VARCHAR(255),              -- Sector or industry targeted (e.g., finance, healthcare)
    affected_assets TEXT[],                  -- List of affected assets or systems
    attack_vector VARCHAR(255),              -- Method used in the attack (e.g., phishing, ransomware, APT)

    -- Calculated/Derived Fields (metrics and calculated insights)
    risk_score INTEGER,                      -- Calculated risk score (e.g., 1-100) based on impact and likelihood
    impact_assessment TEXT,                  -- Summary of the potential impact (business impact, data loss)
    mitigation_effort INTEGER,               -- Estimated mitigation effort (e.g., hours of work, resources)
    estimated_cost DECIMAL(12, 2),           -- Calculated cost of mitigation or loss in USD
    incident_duration INTERVAL,              -- Duration of the incident (calculated from timestamps)
    threat_level VARCHAR(50),                -- Calculated threat level (low, medium, high)
    additional_context JSONB,                -- Additional context or analysis as structured JSON (e.g., OSINT data)
    
    -- Intelligence Summary (human-readable)
    executive_summary TEXT,                  -- High-level summary for C-level executives
    analyst_notes TEXT                       -- Detailed notes or observations from the analyst
);

-- Indexes for faster querying and analytics
CREATE INDEX idx_intelligence_report_event_id ON intelligence_reports (event_id);
CREATE INDEX idx_intelligence_report_risk_score ON intelligence_reports (risk_score);
CREATE INDEX idx_intelligence_report_threat_level ON intelligence_reports (threat_level);
