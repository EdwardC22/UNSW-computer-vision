import { Container } from "@chakra-ui/react";
import { Outlet, useParams } from "react-router-dom";
import MenuHeader from "../components/MenuHeader";

/// Outlet component, renders the menu header, then some component inside,
/// Either menu, basket, individual item or progress

const MenuRouter = () => {
  const { tableNumber } = useParams();
  return (
    <Container>
      {tableNumber !== undefined && <MenuHeader />}
      <Outlet />
    </Container>
  );
};

export default MenuRouter;
