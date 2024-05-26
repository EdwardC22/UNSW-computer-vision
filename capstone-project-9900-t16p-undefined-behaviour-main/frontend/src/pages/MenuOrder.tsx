import { Center, Container, Spinner } from "@chakra-ui/react";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { apiCall } from "../utils/helpers";
import Menu from "../components/Menu";

const MenuOrder = () => {
  const [menu, setMenu] = useState<Array<DCategory>>([]);
  const { restaurantName, tableNumber } = useParams();
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  useEffect(() => {
    async function getMenu() {
      setLoading(true);
      try {
        const menu: any = await apiCall(`/${restaurantName}`, {}, "GET");
        setMenu(menu);
      } catch (err) {
        console.log("Error", err);
      }
      setLoading(false);
    }

    async function validateTableNumber() {
      apiCall(`/${restaurantName}/tables`, {}, "GET")
        .then((res: any) => {
          const table: string = tableNumber === undefined ? "" : tableNumber;
          if (tableNumber === "") {
            navigate(`/${restaurantName}/order`);
          }
          const tableNum = parseInt(table);
          if (tableNum < 1 || tableNum > res.tables) {
            navigate(`/${restaurantName}/order`);
          }
        })
        .catch((err) => console.log(err));
    }
    validateTableNumber();
    getMenu();
  }, []);
  return (
    <Container padding="0">
      {loading ? (
        <Center>
          <Spinner color="purple" thickness="4px" size={"xl"} />
        </Center>
      ) : (
        <Menu categories={menu} />
      )}
    </Container>
  );
};

export default MenuOrder;
