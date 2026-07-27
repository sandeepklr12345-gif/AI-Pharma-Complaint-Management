import { configureStore } from '@reduxjs/toolkit'
import complaintFormReducer from './complaintFormSlice'
import aiCopilotReducer from './aiCopilotSlice'
import complaintsListReducer from './complaintsListSlice'

export const store = configureStore({
  reducer: {
    complaintForm: complaintFormReducer,
    aiCopilot: aiCopilotReducer,
    complaintsList: complaintsListReducer,
  },
})
