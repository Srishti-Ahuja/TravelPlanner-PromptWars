import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChatBox from '../../frontend/src/components/Chat/ChatBox';
import axios from 'axios';

vi.mock('axios');

describe('ChatBox Component', () => {
  it('should debounce search input for 500ms', async () => {
    const onMarkersUpdate = vi.fn();
    const onIntentUpdate = vi.fn();
    
    axios.post.mockResolvedValue({ data: { markers: [], intent: 'test' } });

    render(<ChatBox onMarkersUpdate={onMarkersUpdate} onIntentUpdate={onIntentUpdate} />);
    
    const input = screen.getByPlaceholderText(/Where would you like to go/i);
    
    fireEvent.change(input, { target: { value: 'Japan trip' } });
    
    // Should not have called axios immediately
    expect(axios.post).not.toHaveBeenCalled();
    
    // Wait for debounce
    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(expect.any(String), { query: 'Japan trip' });
    }, { timeout: 1000 });
  });

  it('should show loading state while fetching', async () => {
    axios.post.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));
    
    render(<ChatBox onMarkersUpdate={() => {}} onIntentUpdate={() => {}} />);
    const input = screen.getByPlaceholderText(/Where would you like to go/i);
    
    fireEvent.change(input, { target: { value: 'Testing loading' } });
    
    await waitFor(() => {
      expect(screen.getByText(/Orbit is exploring/i)).toBeDefined();
    });
  });
});
