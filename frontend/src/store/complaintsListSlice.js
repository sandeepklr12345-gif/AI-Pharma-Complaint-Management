import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import apiClient from '../api/client'

export const fetchComplaints = createAsyncThunk(
  'complaintsList/fetch',
  async () => {
    const { data } = await apiClient.get('/api/complaints')
    return data
  }
)

export const saveComplaint = createAsyncThunk(
  'complaintsList/save',
  async (payload) => {
    const { data } = await apiClient.post('/api/complaints', payload)
    return data
  }
)

const initialState = {
  items: [],
  status: 'idle', // idle | loading | error
  error: null,
}

const complaintsListSlice = createSlice({
  name: 'complaintsList',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchComplaints.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(fetchComplaints.fulfilled, (state, action) => {
        state.status = 'idle'
        state.items = action.payload
      })
      .addCase(fetchComplaints.rejected, (state, action) => {
        state.status = 'error'
        state.error = action.error.message
      })
      .addCase(saveComplaint.fulfilled, (state, action) => {
        state.items.unshift(action.payload)
      })
  },
})

export default complaintsListSlice.reducer
