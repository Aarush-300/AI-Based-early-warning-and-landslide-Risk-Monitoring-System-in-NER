import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setActiveRegion } from '../store/navigationSlice';
import { Compass } from 'lucide-react';

export default function SubNav({ states = [] }) {
  const dispatch = useDispatch();
  const activeRegion = useSelector((state) => state.navigation.activeRegion);

  return (
    <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-[1000] flex flex-wrap items-center justify-center gap-2 p-2 bg-slate-900/80 backdrop-blur-xl rounded-full border border-slate-700/50 shadow-[0_8px_30px_rgb(0,0,0,0.4)] w-max max-w-[95%] transition-all duration-300">
      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-3 flex items-center gap-1.5">
        <Compass className="h-3.5 w-3.5 text-blue-400" />
        Jump to State:
      </span>
      
      <button
        onClick={() => dispatch(setActiveRegion(null))}
        className={`px-3 py-1.5 text-xs font-bold rounded-full transition-all duration-300 ${
          activeRegion === null 
            ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 shadow-md shadow-orange-500/20' 
            : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
        }`}
      >
        All NER (Overview)
      </button>
      
      {states.map((st) => {
        const isActive = activeRegion === st.name;
        return (
          <button
            key={st.name}
            onClick={() => dispatch(setActiveRegion(st.name))}
            className={`px-3 py-1.5 text-xs font-semibold rounded-full transition-all duration-300 ${
              isActive 
                ? 'bg-slate-700/80 text-white shadow-inner border border-slate-600' 
                : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
            }`}
          >
            {st.name}
          </button>
        );
      })}
    </div>
  );
}

