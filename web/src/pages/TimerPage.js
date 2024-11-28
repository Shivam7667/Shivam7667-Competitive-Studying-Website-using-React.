import React from 'react';
import StudyTimer from '../components/StudyTimer';
import StudyHistory from '../components/StudyHistory';

function TimerPage() {
  return (
    <div>
      <h1>Study Timer</h1>
      <StudyTimer />
      <h2>Study History</h2>
      <StudyHistory />
    </div>
  );
}

export default TimerPage;
