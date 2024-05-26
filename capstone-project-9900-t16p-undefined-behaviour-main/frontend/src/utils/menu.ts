export function getOrder(restaurantName: string) {
  let order = localStorage.getItem(restaurantName);
  if (order === null) {
    return [];
  }
  return JSON.parse(order);
}

interface ShortItem {
  name: string;
  cost: number;
  id: number;
}
export function setOrder(
  restaurantName: any,
  item: ShortItem,
  quantity: number
) {
  const order: Array<[ShortItem, number]> = getOrder(restaurantName); // Either partially complete array or empty
  const itemIndex = order.findIndex((element) => element[0].id === item.id);
  if (itemIndex === -1) {
    order.push([{ name: item.name, cost: item.cost, id: item.id }, quantity]);
  } else {
    let item = order[itemIndex];
    order[itemIndex] = [item[0], item[1] + quantity];
  }
  const final = order.filter((item) => item[1] > 0);
  localStorage.setItem(restaurantName, JSON.stringify(final));
}
