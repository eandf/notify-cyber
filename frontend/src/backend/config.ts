// backend configuration info

const config = {
  max_array_str_size: 3000,
  valid_sources: [
    {
      name: "CISA",
      id: "caisa",
    },
    {
      name: "Dark Reading",
      id: "dr",
    },
    {
      name: "The Hacker News",
      id: "thn",
    },
    {
      name: "IT Security Guru",
      id: "isg",
    },
    {
      name: "CVE",
      id: "cve",
    },
  ],
  valid_input_keys: ["sources", "after", "filter"],
  max_limit: 100,
  max_days_back: 365,
  limitWaitMinutes: 15,
  maxRequestsLimit: 50,
};

export default config;
