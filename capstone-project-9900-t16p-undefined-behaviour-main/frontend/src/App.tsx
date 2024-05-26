import * as React from "react";
import { Button, ChakraProvider, useColorMode } from "@chakra-ui/react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";
import StaffPortal from "./pages/StaffPortal";
import theme from "./theme";
import MenuOrder from "./pages/MenuOrder";
import MenuRouter from "./pages/MenuRouter";
import MenuTableSelect from "./components/MenuTableSelect";
import ItemCard from "./components/ItemCard";
import MenuItemCard from "./components/MenuItemCard";
import Basket from "./pages/Basket";
import OrderProgress from "./pages/OrderProgress";
import KitchenDashboard from "./pages/KitchenDashboard";
import WaitStaffDashboard from "./pages/WaitStaffDashboard";
import Analytics from "./pages/Analytics";

export const App = () => (
  <ChakraProvider theme={theme}>
    <Router>
      <Routes>
        <Route path="/" element={<Register />} />
        <Route path="/:restaurantName">
          <Route path="staff" element={<StaffPortal />} />
          <Route path="staff/wait" element={<WaitStaffDashboard />} />
          <Route path="staff/kitchen" element={<KitchenDashboard />} />
          <Route path="staff/manager">
            <Route index element={<Login />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="analytics" element={<Analytics />} />
          </Route>
          <Route path="order" element={<MenuRouter />}>
            <Route
              path="/:restaurantName/order"
              element={<MenuTableSelect />}
            />
            <Route
              path="/:restaurantName/order/:tableNumber"
              element={<MenuOrder />}
            />
            <Route
              path="/:restaurantName/order/:tableNumber/:itemName"
              element={<MenuItemCard />}
            />
            <Route
              path="/:restaurantName/order/:tableNumber/basket"
              element={<Basket />}
            />
            <Route
              path="/:restaurantName/order/:tableNumber/progress"
              element={<OrderProgress />}
            />
          </Route>
        </Route>
        <Route path="*" element={<div>No page match</div>} />
      </Routes>
    </Router>
  </ChakraProvider>
);
