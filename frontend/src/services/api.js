const API_BASE_URL = "http://127.0.0.1:8000";


export async function predictFood(foodData) {

  const response = await fetch(
    `${API_BASE_URL}/api/v1/predict`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(foodData),
    }
  );


  if (!response.ok) {

    const errorData = await response.json()
      .catch(() => null);

    throw new Error(
      errorData?.detail ||
      "Prediction request failed."
    );
  }


  return await response.json();
}


export async function askNutritionist(question) {

  const response = await fetch(
    `${API_BASE_URL}/chat/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question,
      }),
    }
  );


  if (!response.ok) {

    const errorData = await response.json()
      .catch(() => null);

    throw new Error(
      errorData?.detail ||
      "Chat request failed."
    );
  }


  return await response.json();
}