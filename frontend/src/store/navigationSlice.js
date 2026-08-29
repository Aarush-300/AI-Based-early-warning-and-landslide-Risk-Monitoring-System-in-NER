import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  activeModule: 'map',
  activeRegion: null, // null means 'All NER'
};

const navigationSlice = createSlice({
  name: 'navigation',
  initialState,
  reducers: {
    setActiveModule: (state, action) => {
      state.activeModule = action.payload;
    },
    setActiveRegion: (state, action) => {
      state.activeRegion = action.payload;
    },
  },
});

export const { setActiveModule, setActiveRegion } = navigationSlice.actions;
export default navigationSlice.reducer;

