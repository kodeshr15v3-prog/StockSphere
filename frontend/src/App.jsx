import React, { useEffect, useState, useRef } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Toaster, toast } from 'react-hot-toast';
import io from 'socket.io-client';

import {
  fetchCurrentUser,
  setInitialLoadingDone,
} from './store/slices/authSlice';
import { addLiveNotification } from './store/slices/notificationSlice';
import { updateStockPrice } from './store/slices/stocksSlice';

import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import { SocketContext } from './context/SocketContext';

import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import MarketPage from './pages/MarketPage';
import WatchlistPage from './pages/WatchlistPage';
import StockDetailPage from './pages/StockDetailPage';
import PortfolioPage from './pages/PortfolioPage';
import CommunityPage from './pages/CommunityPage';
import ProfilePage from './pages/ProfilePage';

function App() {
  const dispatch = useDispatch();

  const { user, token, initialLoading } = useSelector(
    (state) => state.auth
  );

  const { quotes } = useSelector((state) => state.stocks);

  const [socket, setSocket] = useState(null);
  const subscribedSymbols = useRef(new Set());

  // Check authentication
  useEffect(() => {
    if (token) {
      dispatch(fetchCurrentUser());
    } else {
      dispatch(setInitialLoadingDone());
    }
  }, [dispatch, token]);

  // Socket connection
  useEffect(() => {
    if (!user) return;

    const socketInstance = io(
      import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000',
      {
        transports: ['websocket', 'polling'],
      }
    );

    setSocket(socketInstance);

    // Join user room
    socketInstance.emit('join_user', user._id);

    // Notification handler
    const handleNotification = (notif) => {
      dispatch(addLiveNotification(notif));

      toast(`🔔 ${notif.message}`, {
        icon: '🔔',
        style: {
          background: '#1a2235',
          color: '#fff',
          border: '1px solid #2a3548',
        },
      });
    };

    // Stock price handler
    const handlePriceUpdate = (data) => {
      dispatch(updateStockPrice(data));
    };

    socketInstance.on('new_notification', handleNotification);
    socketInstance.on('stock_price_update', handlePriceUpdate);

    return () => {
      socketInstance.off('new_notification', handleNotification);
      socketInstance.off('stock_price_update', handlePriceUpdate);
      socketInstance.disconnect();
      setSocket(null);
      subscribedSymbols.current.clear();
    };
  }, [user, dispatch]);

  // Subscribe to stock rooms
  useEffect(() => {
    if (!socket || !quotes) return;

    Object.keys(quotes).forEach((symbol) => {
      if (!subscribedSymbols.current.has(symbol)) {
        socket.emit('join_stock', symbol);
        subscribedSymbols.current.add(symbol);
      }
    });
  }, [socket, quotes]);

  // Loading
  if (initialLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        Loading...
      </div>
    );
  }

  return (
    <>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#1a2235',
            color: '#fff',
            border: '1px solid #2a3548',
          },
          success: {
            iconTheme: {
              primary: '#00d4aa',
              secondary: '#080c14',
            },
          },
          error: {
            iconTheme: {
              primary: '#ff4d6d',
              secondary: '#fff',
            },
          },
        }}
      />

      <SocketContext.Provider value={socket}>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/market" element={<MarketPage />} />
              <Route path="/watchlist" element={<WatchlistPage />} />
              <Route path="/portfolio" element={<PortfolioPage />} />
              <Route path="/community" element={<CommunityPage />} />
              <Route path="/profile/:id" element={<ProfilePage />} />
              <Route path="/stocks/:symbol" element={<StockDetailPage />} />
              <Route path="/stock/:symbol" element={<StockDetailPage />} />
            </Route>
          </Route>

          {/* Redirects */}
          <Route
            path="/"
            element={<Navigate to="/dashboard" replace />}
          />
          <Route
            path="*"
            element={<Navigate to="/dashboard" replace />}
          />
        </Routes>
      </SocketContext.Provider>
    </>
  );
}

export default App;