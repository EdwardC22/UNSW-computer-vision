import {
  Accordion,
  Box,
  Button,
  ButtonGroup,
  Center,
  Container,
  Flex,
  Heading,
  Icon,
  IconButton,
  Select,
  Spinner,
  Tooltip,
  useDisclosure,
} from "@chakra-ui/react";
import { useNavigate, useParams } from "react-router-dom";
import EditableCategory from "../components/EditableCategory";
import PopupForm from "../components/PopupForm";
import { useEffect, useState } from "react";
import FormField from "../components/FormField";
import { createDFormObject } from "../utils/data";
import { apiCall, decodeRestaurantName } from "../utils/helpers";
import { AddIcon, QuestionIcon } from "@chakra-ui/icons";
import ThemeToggle from "../components/ThemeToggle";
import DeleteButton from "../components/DeleteButton";
import { Link as RouterLink } from "react-router-dom";

function Dashboard() {
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();
  let { restaurantName } = useParams();
  useEffect(() => {
    function verifyAccess() {
      apiCall(`/${restaurantName}/verifytoken`, {}, "POST").catch((err) => {
        console.log(err);
        navigate(`../`);
      });
    }
    verifyAccess();
  }, [restaurantName, navigate]);

  const addCategory = async () => {
    setPopupFormState(
      createDFormObject(
        "Add a category",
        { categoryName: "" },
        [
          <FormField
            key={"categoryName"}
            id="categoryName"
            label="Enter Category Name:"
            required={true}
          />,
        ],
        (values: any) => {
          if (values.categoryName.trim().length === 0) {
            alert("Category name cannot be empty");
            return;
          }
          apiCall(
            `/${restaurantName}/createcategory`,
            {
              name: values.categoryName,
            },
            "POST"
          )
            .then((res) => {
              getMenu();
              onClose();
            })
            .catch((err) => alert(`Error adding new category: ${err.error}`));
        }, //submit handler
        undefined,
        onClose
      )
    );
    // Set data then open
    onOpen();
  };

  const [currDrag, setCurrDrag] = useState<number | undefined>(undefined);
  const [itemDrag, setItemDrag] = useState<number | undefined>(undefined);
  function handleDrag(ev: any, key: number) {
    setCurrDrag(key); // key is the id of the category
    setItemDrag(undefined);
  }
  function handleDrop(ev: any) {
    const dragBox = menu.find((category) => category.id === currDrag);
    const dropBox = menu.find(
      (category) =>
        category.id ===
        parseInt(
          ev.currentTarget.id.substring(
            ev.currentTarget.id.lastIndexOf("c") + 1
          )
        )
    );
    // Switch categories
    if (dropBox && itemDrag) {
      apiCall(
        `/${restaurantName}/edititemcat/${itemDrag}`,
        { new_category: dropBox.id },
        "PUT"
      )
        .then((res) => getMenu())
        .catch((err) => alert(`Error updating category of item: ${err.error}`));
    }

    if (!dragBox || !dropBox) return;
    if (dragBox.id !== dropBox.id) {
      apiCall(
        `/${restaurantName}/editcategorypos/${dragBox.id}`,
        {
          new_position: dropBox.restaurant_pos,
        },
        "PUT"
      )
        .then((_) => getMenu())
        .catch((err) => console.log(err));
    }
    setCurrDrag(undefined);
  }

  const [menu, setMenu] = useState<Array<DCategory>>([]);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [popupFormState, setPopupFormState] = useState<
    DPopupFormState | undefined
  >();
  async function getMenu() {
    // Noexcept
    try {
      const menu: any = await apiCall(`/${restaurantName}`, {}, "GET");
      setMenu(menu);
      setLoading(false);
    } catch (err) {
      console.log("Error", err);
    }
  }
  useEffect(() => {
    getMenu();
  }, []);

  const setTables = (value: string) => {
    if (value.trim().length === 0) return;
    const val = parseInt(value);
    apiCall(`/${restaurantName}/tables`, { tables: val }, "POST").catch((err) =>
      alert(err.error)
    );
  };
  return (
    <Container maxWidth="1275px" display="flex" flexDir="column" gap="15px">
      <Box display="flex" justifyContent={"space-between"}>
        <Heading textAlign={"center"}>
          Manage {decodeRestaurantName(restaurantName)} Menu
        </Heading>
        <ButtonGroup alignItems={"center"}>
          <Tooltip
            fontSize="md"
            label="The order of categories and items can be changed by dragging and dropping!"
          >
            <QuestionIcon boxSize={5} />
          </Tooltip>
          <ThemeToggle />
        </ButtonGroup>
      </Box>
      <Flex justifyContent={"space-between"}>
        <Button colorScheme={"teal"} as={RouterLink} to="../analytics">
          Analytics
        </Button>
        <Flex dir="column" gap="5px">
          <Select
            placeholder="Seating Capacity"
            onChange={(ev) => setTables(ev.target.value)}
          >
            {Array(100)
              .fill(0)
              .map((_, idx) => {
                return (
                  <option value={idx + 1} key={`tableSelect${idx + 1}`}>
                    {idx + 1}
                  </option>
                );
              })}
          </Select>
          <Button
            colorScheme={"gray"}
            onClick={() => {
              apiCall("/logout", {}, "POST");
              navigate(`/${restaurantName}/staff`);
            }}
          >
            Log out
          </Button>
        </Flex>
      </Flex>
      <Box>
        {loading ? (
          <Center>
            <Spinner color="purple" thickness="4px" size={"xl"} />
          </Center>
        ) : (
          <Accordion allowMultiple defaultIndex={[0]}>
            {menu.map((category) => (
              <EditableCategory
                handleDrag={handleDrag}
                handleDrop={handleDrop}
                setItemDrag={setItemDrag}
                key={`${restaurantName}${category.id}`}
                name={category.name}
                items={category.items}
                cId={category.id}
                getMenu={getMenu}
                deleteButton={
                  <DeleteButton
                    clickHandler={() => {
                      apiCall(
                        `/${restaurantName}/deletecategory/${category.id}`,
                        {},
                        "DELETE"
                      )
                        .then((_) => {
                          getMenu();
                          onClose();
                        })
                        .catch((err) =>
                          alert(`Unable to delete category: Error: ${err}`)
                        );
                    }}
                  />
                }
              />
            ))}
          </Accordion>
        )}
      </Box>
      <Box display="flex" justifyContent={"flex-end"}>
        <Button
          rightIcon={<AddIcon />}
          colorScheme={"teal"}
          onClick={addCategory}
        >
          Add Category
        </Button>
      </Box>
      {isOpen && (
        <PopupForm
          handleClose={onClose}
          open={isOpen}
          formState={popupFormState}
        />
      )}
    </Container>
  );
}

export default Dashboard;
