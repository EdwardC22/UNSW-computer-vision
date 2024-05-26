import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
  Flex,
  Box,
  FormControl,
  FormLabel,
  Textarea,
  ButtonGroup,
  Image,
} from "@chakra-ui/react";
import { Field, Formik } from "formik";
import { useState } from "react";
import { useParams } from "react-router-dom";
import { apiCall, fileToDataUrl } from "../utils/helpers";
import FormField from "./FormField";

/// Main form component used to update the properties of an existing item or
/// to create a new item
const isEmpty = (field: string) => {
  return field.trim().length === 0;
};
interface Props {
  title: string;
  item: DItem; // New item pass empty object
  open: boolean;
  handleClose: Function;
  deleteButton?: any;
  buttonText: string;
  categoryID: number;
  getMenu: Function;
  buttonIcon?: any;
}

const ItemForm = ({
  title,
  item,
  open,
  handleClose,
  buttonText,
  deleteButton,
  categoryID,
  getMenu,
  buttonIcon,
}: Props) => {
  let { restaurantName } = useParams();
  const [newImage, setNewImage] = useState("");
  async function setImage(ev: any) {
    if (!ev.target.files) {
      return;
    }
    const file = ev.target.files[0];
    if (file) {
      const data: any = await fileToDataUrl(file);
      setNewImage(data);
    }
  }
  function closeModal() {
    setNewImage("");
    handleClose();
  }
  return (
    <Modal size="2xl" isOpen={open} onClose={closeModal}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>{title}</ModalHeader>
        <ModalCloseButton />
        <Formik
          initialValues={item}
          onSubmit={(values, actions) => {
            if (
              isEmpty(values.name) ||
              isEmpty(values.description) ||
              isEmpty(values.ingredients)
            ) {
              alert("Name, description or ingredients cannot be empty");
              return;
            }
            apiCall(
              item.id === -1
                ? `/${restaurantName}/createitem`
                : `/${restaurantName}/edititem/${item.id}`,
              {
                name: values.name,
                description: values.description,
                ingredients: values.ingredients,
                cost: values.cost,
                categoryID: categoryID,
                image: newImage === "" ? item.image : newImage,
              },
              item.id === -1 ? "POST" : "PUT"
            )
              .then((res) => {
                getMenu();
                closeModal();
              })
              .catch((err) =>
                alert(
                  `Error ${item.id === -1 ? "creating" : "updaing"} item: ${
                    err.error
                  }`
                )
              );
          }}
        >
          {({ handleSubmit, errors, touched, values }) => (
            <form onSubmit={handleSubmit}>
              <ModalBody>
                <Flex gap="10px">
                  <Box flex="1">
                    <FormField
                      id="name"
                      label="Enter item name: "
                      required={true}
                    />
                    <FormControl>
                      <FormLabel htmlFor={"description"}>
                        Enter item description:
                      </FormLabel>
                      <Field
                        as={Textarea}
                        id="description"
                        name="description"
                        required={true}
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel htmlFor={"ingredients"}>
                        Enter item ingredients:
                      </FormLabel>
                      <Field
                        as={Textarea}
                        id="ingredients"
                        name="ingredients"
                        required={true}
                      />
                    </FormControl>
                  </Box>
                  <Box flex="1" display="flex" flexDir="column">
                    <FormControl>
                      <Flex flexDir="column">
                        <Flex gap="10px" flex="1">
                          {item.image && (
                            <Image
                              src={item.image}
                              alt="original"
                              boxSize="150px"
                            />
                          )}
                          {newImage && (
                            <Image src={newImage} alt="new" boxSize="150px" />
                          )}
                        </Flex>
                        <FormLabel htmlFor={"imageUpload"}>
                          Upload Image
                        </FormLabel>
                        <input
                          id="imageUpload"
                          name="imageUpload"
                          type="file"
                          onChange={(ev) => {
                            setImage(ev);
                          }}
                        />
                      </Flex>
                    </FormControl>
                    <FormField
                      id="cost"
                      label="Enter cost:"
                      type={"number"}
                      required={true}
                    />
                  </Box>
                </Flex>
              </ModalBody>
              <ModalFooter justifyContent={"space-between"}>
                <Box>{deleteButton}</Box>
                <ButtonGroup>
                  <Button onClick={closeModal}>Cancel</Button>
                  <Button
                    rightIcon={buttonIcon}
                    type="submit"
                    colorScheme={"teal"}
                  >
                    {buttonText}
                  </Button>
                </ButtonGroup>
              </ModalFooter>
            </form>
          )}
        </Formik>
      </ModalContent>
    </Modal>
  );
};

export default ItemForm;
