import React, { useState } from "react";
import type { BirthInfo } from "../../types/tuvi";

interface InputFormProps {
  onSuccess: (data: BirthInfo) => void;
}

const InputForm: React.FC<InputFormProps> = ({ onSuccess }) => {
  const [calendarType, setCalendarType] = useState<'duong' | 'am'>('am');
  const [form, setForm] = useState({
    gioi_tinh: 'Nữ',
    gio_sinh: '15:00',
    ngay: '15',
    thang: '1',
    nam: '2000'
  });
  const [error, setError] = useState<string>('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setError('');
    setForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      // Validate required fields
      if (!form.gioi_tinh || !form.gio_sinh || !form.ngay || !form.thang || !form.nam) {
        throw new Error('Vui lòng điền đầy đủ thông tin');
      }

      // Convert hour from "HH:mm" format to number
      const [hours] = form.gio_sinh.split(':').map(Number);
      if (isNaN(hours) || hours < 0 || hours > 23) {
        throw new Error('Giờ sinh không hợp lệ');
      }

      // Parse and validate numeric fields
      const ngay = parseInt(form.ngay);
      const thang = parseInt(form.thang);
      const nam = parseInt(form.nam);

      if (isNaN(ngay) || isNaN(thang) || isNaN(nam)) {
        throw new Error('Ngày tháng năm phải là số');
      }

      const submitData: BirthInfo = {
        gioi_tinh: form.gioi_tinh,
        gio_sinh: hours,
        ...(calendarType === 'duong' ? {
          ngay_dl: ngay,
          thang_dl: thang,
          nam_dl: nam
        } : {
          ngay_al: ngay,
          thang_al: thang,
          nam_al: nam
        })
      };

      onSuccess(submitData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Có lỗi xảy ra');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: '0 auto', padding: 16, border: '1px solid #eee', borderRadius: 8 }}>
      {error && (
        <div style={{ color: 'red', marginBottom: 12, padding: 8, background: '#fff4f4', borderRadius: 4 }}>
          {error}
        </div>
      )}
      <div style={{ marginBottom: 12 }}>
        <label>
          <input
            type="radio"
            name="calendarType"
            value="duong"
            checked={calendarType === 'duong'}
            onChange={(e) => setCalendarType(e.target.value as 'duong' | 'am')}
          />
          Dương lịch
        </label>
        <label style={{ marginLeft: 16 }}>
          <input
            type="radio"
            name="calendarType"
            value="am"
            checked={calendarType === 'am'}
            onChange={(e) => setCalendarType(e.target.value as 'duong' | 'am')}
          />
          Âm lịch
        </label>
      </div>

      <div style={{ marginBottom: 12 }}>
        <label>Giới tính:
          <select
            name="gioi_tinh"
            value={form.gioi_tinh}
            onChange={handleChange}
            required
            style={{ marginLeft: 8 }}
          >
            <option value="">Chọn</option>
            <option value="Nam">Nam</option>
            <option value="Nữ">Nữ</option>
          </select>
        </label>
      </div>

      <div style={{ marginBottom: 12 }}>
        <label>Giờ sinh:
          <input
            type="time"
            name="gio_sinh"
            value={form.gio_sinh}
            onChange={handleChange}
            required
            style={{ marginLeft: 8 }}
          />
        </label>
      </div>

      <div style={{ marginBottom: 12 }}>
        <label>Ngày:
          <input
            name="ngay"
            type="number"
            min="1"
            max={calendarType === 'duong' ? "31" : "30"}
            value={form.ngay}
            onChange={handleChange}
            required
            style={{ marginLeft: 8, width: 60 }}
          />
        </label>
        <label style={{ marginLeft: 12 }}>Tháng:
          <input
            name="thang"
            type="number"
            min="1"
            max="12"
            value={form.thang}
            onChange={handleChange}
            required
            style={{ marginLeft: 8, width: 60 }}
          />
        </label>
        <label style={{ marginLeft: 12 }}>Năm:
          <input
            name="nam"
            type="number"
            min="1900"
            max={new Date().getFullYear()}
            value={form.nam}
            onChange={handleChange}
            required
            style={{ marginLeft: 8, width: 80 }}
          />
        </label>
      </div>

      <button
        type="submit"
        style={{
          padding: '8px 16px',
          background: '#1976d2',
          color: '#fff',
          border: 'none',
          borderRadius: 4,
          cursor: 'pointer'
        }}
      >
        Lập Lá Số
      </button>
    </form>
  );
};

export default InputForm;
