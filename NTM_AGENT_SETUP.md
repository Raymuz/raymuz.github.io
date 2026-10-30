# NTM AI Agent — website integration

The full-screen project page is at `projects/ntm-ai-agent/index.html` and the configuration at `assets/ntm-agent-config.js`.

Current Hugging Face Space: https://huggingface.co/spaces/raymuz/ntm-ai-assistant
Expected embedding host: https://raymuz-ntm-ai-assistant.hf.space/

**Space visibility provided by the owner: Private.** `NTM_AGENT_PUBLIC` intentionally remains `false`, so visitors see an access notice rather than an inaccessible login frame.

After you verify no secrets/private data are exposed, make the Space Public in HF Settings, confirm it is running and can be embedded; then set `window.NTM_AGENT_PUBLIC = true` in `assets/ntm-agent-config.js` and publish the website update. The Space API key remains in Hugging Face Secrets; never put it in public HTML or JS.

The page uses almost the full viewport for the agent, with minimal header and links to the portfolio and NTM business website. This does not modify ntmcm.com.
