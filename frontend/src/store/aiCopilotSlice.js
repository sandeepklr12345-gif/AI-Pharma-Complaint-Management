import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import apiClient from '../api/client'

export const uploadFile = createAsyncThunk(
  'aiCopilot/uploadFile',
  async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const { data } = await apiClient.post('/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return data // { text, file_type }
  }
)

export const analyzeText = createAsyncThunk(
  'aiCopilot/analyzeText',
  async (text) => {
    const { data } = await apiClient.post('/api/analyze', { text })
    return data // AnalyzeResponse
  }
)

const initialState = {
  inputText: '',
  uploadedFileName: null,
  status: 'idle', // idle | uploading | analyzing | done | error
  result: null,
  error: null,
}

const aiCopilotSlice = createSlice({
  name: 'aiCopilot',
  initialState,
  reducers: {
    setInputText(state, action) {
      state.inputText = action.payload
    },
    clearResult(state) {
      state.result = null
      state.status = 'idle'
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(uploadFile.pending, (state) => {
        state.status = 'uploading'
        state.error = null
      })
      .addCase(uploadFile.fulfilled, (state, action) => {
        state.inputText = action.payload.text
        state.status = 'idle'
      })
      .addCase(uploadFile.rejected, (state, action) => {
        state.status = 'error'
        state.error = action.error.message || 'File upload failed'
      })
      .addCase(analyzeText.pending, (state) => {
        state.status = 'analyzing'
        state.error = null
      })
      .addCase(analyzeText.fulfilled, (state, action) => {
        state.status = 'done'
        state.result = action.payload
      })
      .addCase(analyzeText.rejected, (state, action) => {
        state.status = 'error'
        state.error = action.error.message || 'Analysis failed'
      })
  },
})

export const { setInputText, clearResult } = aiCopilotSlice.actions
export default aiCopilotSlice.reducer
