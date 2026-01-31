import axios from "axios";

// Direct backend URL to bypass proxy issues
const API_BASE_URL = "http://127.0.0.1:8000";
console.log("DEBUG: Using API URL:", API_BASE_URL);

export const detectFile = async (files) => {
  const formData = new FormData();

  // Append all files with the key 'files' (must match backend parameter name)
  if (files.length) {
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }
  } else {
    // Fallback if single file is passed (though we should always pass list/array-like)
    formData.append("files", files);
  }

  const response = await axios.post(
    `${API_BASE_URL}/detect`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 600000, // 10 minutes
      maxBodyLength: Infinity,
      maxContentLength: Infinity,
    }
  );

  return response.data;
};
