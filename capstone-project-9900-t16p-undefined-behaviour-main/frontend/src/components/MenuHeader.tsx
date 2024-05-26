import { ArrowBackIcon, BellIcon } from "@chakra-ui/icons";
import { ButtonGroup, Flex, IconButton, Link, Tooltip } from "@chakra-ui/react";
import { FaPhone, FaShoppingBasket } from "react-icons/fa";
import { useNavigate, useParams } from "react-router-dom";
import { apiCall, decodeRestaurantName } from "../utils/helpers";
import { Link as RouterLink } from "react-router-dom";

/// Component used as the header for all customer ordering pages after the table has
/// been selected

const MenuHeader = () => {
  const { restaurantName, tableNumber } = useParams();
  const navigate = useNavigate();
  return (
    <Flex justifyContent="space-between">
      <IconButton
        aria-label="Back button"
        icon={<ArrowBackIcon />}
        onClick={() => window.history.back()}
      />
      <Link
        variant="ghost"
        as={RouterLink}
        to={`/${restaurantName}/order/${tableNumber}`}
        fontSize="1.5rem"
      >
        {decodeRestaurantName(restaurantName)} Menu
      </Link>
      <ButtonGroup>
        <Tooltip label="Request assistance">
          <IconButton
            onClick={() =>
              apiCall(
                `/${restaurantName}/${tableNumber}/assistance`,
                { bill: false },
                "POST"
              )
                .then((res) => console.log(res))
                .catch((err) => alert(`Error requesting help: ${err}`))
            }
            aria-label="Request Assistance"
            icon={<FaPhone />}
          />
        </Tooltip>
        <Tooltip label="Basket">
          <IconButton
            aria-label="Goto Basket"
            icon={<FaShoppingBasket />}
            onClick={() =>
              navigate(`/${restaurantName}/order/${tableNumber}/basket`)
            }
          />
        </Tooltip>
        <Tooltip label="Order progress">
          <IconButton
            aria-label="Check order progress"
            icon={<BellIcon />}
            onClick={() =>
              navigate(`/${restaurantName}/order/${tableNumber}/progress`)
            }
          />
        </Tooltip>
      </ButtonGroup>
    </Flex>
  );
};

export default MenuHeader;
