import { createSlice } from '@reduxjs/toolkit'

const emptyForm = {
  complaint_id: '',
  customer_name: '',
  product_name: '',
  batch_number: '',
  category: '',
  description: '',
  country: '',
  severity: '',
  status: 'New',
}

const initialState = {
  fields: { ...emptyForm },
  // tracks which fields were auto-filled by the AI, so the UI can
  // highlight them until the user edits (and thereby "confirms") them
  aiFilledKeys: [],
}

const complaintFormSlice = createSlice({
  name: 'complaintForm',
  initialState,
  reducers: {
    updateField(state, action) {
      const { key, value } = action.payload
      state.fields[key] = value
      // once the user edits it themselves, it's no longer purely AI-filled
      state.aiFilledKeys = state.aiFilledKeys.filter((k) => k !== key)
    },
    fillFromAi(state, action) {
      const extracted = action.payload
      const filledKeys = []
      for (const [key, value] of Object.entries(extracted)) {
        if (value && key in state.fields) {
          state.fields[key] = value
          filledKeys.push(key)
        }
      }
      state.aiFilledKeys = filledKeys
    },
    resetForm(state) {
      state.fields = { ...emptyForm }
      state.aiFilledKeys = []
    },
  },
})

export const { updateField, fillFromAi, resetForm } = complaintFormSlice.actions
export default complaintFormSlice.reducer
