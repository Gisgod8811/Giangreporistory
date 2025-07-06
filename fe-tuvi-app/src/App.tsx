import { useState } from 'react'
import './App.css'
import InputForm from './components/InputForm/InputForm'
import LaSoTuVi from './components/LaSoTuVi/LaSoTuVi'
import type { LaSoData, BirthInfo } from './types/tuvi'
import { createLaSo } from './api/tuviService'

function App() {
  const [laSo, setLaSo] = useState<LaSoData | null>(null);
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSuccess = async (data: BirthInfo) => {
    try {
      setIsLoading(true);
      setError('');
      const response = await createLaSo(data);
      console.log('Received laSo data:', response);
      setLaSo(response);
    } catch (err) {
      console.error('Error creating la so:', err);
      setError(err instanceof Error ? err.message : 'Có lỗi xảy ra khi lập lá số');
      setLaSo(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container" style={{ padding: '20px' }}>
      {error && (
        <div style={{ color: 'red', marginBottom: '20px', padding: '10px', background: '#fff4f4', borderRadius: '4px' }}>
          {error}
        </div>
      )}

      {isLoading ? (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          Đang lập lá số...
        </div>
      ) : laSo === null ? (
        <InputForm onSuccess={handleSuccess} />
      ) : (
        <div>
          <button
            onClick={() => setLaSo(null)}
            style={{ marginBottom: '20px', padding: '8px 16px', cursor: 'pointer' }}
          >
            Lập lá số mới
          </button>
          <LaSoTuVi data={laSo} />
        </div>
      )}
    </div>
  )
}

export default App
