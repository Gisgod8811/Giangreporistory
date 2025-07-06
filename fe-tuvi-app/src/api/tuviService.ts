import type { BirthInfo, LaSoData } from "../types/tuvi";

export async function createLaSo(birthInfo: BirthInfo): Promise<LaSoData> {
  try {
    console.log('Sending data to API:', JSON.stringify(birthInfo, null, 2));

    const response = await fetch("/api/lap-la-so/", { // removed trailing slash
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify(birthInfo),
    });

    const responseText = await response.text();
    console.log('Raw API Response:', responseText);

    if (!response.ok) {
      throw new Error(`API Error ${response.status}: ${responseText}`);
    }

    try {
      const data = JSON.parse(responseText);
      console.log('Parsed API Response:', data);
      return data;
    } catch (parseError) {
      console.error('JSON Parse Error:', parseError);
      throw new Error('Invalid JSON response from server');
    }
  } catch (error) {
    console.error('API Call Error:', error);
    throw error;
  }
}
