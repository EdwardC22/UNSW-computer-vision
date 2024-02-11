#include <iostream>
#include <string>
#include <string_view>
#include <unordered_map>
#include <map>
#include <functional>

struct Engine {
public:
    void new_order(bool is_buy, int price, int quantity, const std::string& id) {
        if (is_buy) {
            quantity = trade(is_buy, price, quantity, id);
            if (quantity > 0) {
                trade_.emplace(id, quantity);
                if (buy_.find(price) == buy_.end()) {
                    buy_[price] = {};
                }
                buy_[price].emplace_back(id);
                std::cout << "INSERT BUY " << id << " " << price << " " << quantity << std::endl;
            }
        }
        else {
            quantity = trade(is_buy, price, quantity, id);
            if (quantity > 0) {
                trade_.emplace(id, quantity);
                if (sell_.find(price) == sell_.end()) {
                    sell_[price] = {};
                }
                sell_[price].emplace_back(id);
                std::cout << "INSERT SELL " << id << " " << price << " " << quantity << std::endl;
            }
        }
        return;

    }

    void modify(const std::string& id, bool is_buy, int price, int quantity) {

    }

    void cancel(const std::string& id) {
        auto tmp = trade_.find(id);
        if (tmp != trade_.end()) {
            trade_.erase(tmp);
            std::cout << "CANCEL " << id << " " << tmp->second << std::endl;
        }
        return;
    }
private:
    std::unordered_map<std::string, int> trade_;
    std::map<int, std::vector<std::string>> sell_;
    std::map<int, std::vector<std::string>, std::greater<int>> buy_;
    auto trade(bool is_buy, int price, int quantity, const std::string& id) -> int {
        if (is_buy) {
            auto p = sell_.equal_range(price);
            for (auto it1 = p.first; it1 != p.second; ++it1) {
                for (auto it2 = it1->second.begin(); it2 != it1->second.end();) {
                    auto tmp = trade_.find(*it2);
                    if (tmp == trade_.end()) {
                        it2 = it1->second.erase(it2);
                        continue;
                    }
                    if (quantity >= trade_[*it2]) {
                        std::cout << "TRADE " << id << " " << *it2 << " " << price << " " << trade_[*it2] << std::endl;
                        quantity -= trade_[*it2];
                        trade_.erase(tmp);
                        it2 = it1->second.erase(it2);
                    }
                    else {
                        std::cout << "TRADE " << id << " " << *it2 << " " << price << " " << quantity << std::endl;
                        trade_[*it2] -= quantity;
                        quantity = 0;
                        break;
                    }
                }
            }
        }
        else {
            auto p = buy_.equal_range(price);
            for (auto it1 = p.first; it1 != p.second; ++it1) {
                for (auto it2 = it1->second.begin(); it2 != it1->second.end();) {
                    auto tmp = trade_.find(*it2);
                    if (tmp == trade_.end()) {
                        it2 = it1->second.erase(it2);
                        continue;
                    }
                    if (quantity >= trade_[*it2]) {

                        std::cout << "TRADE " << id << " " << *it2 << " " << price << " " << trade_[*it2] << std::endl;
                        quantity -= trade_[*it2];
                        trade_.erase(tmp);
                        it2 = it1->second.erase(it2);
                    }
                    else {
                        std::cout << "TRADE " << id << " " << *it2 << " " << price << " " << quantity << std::endl;
                        trade_[*it2] -= quantity;
                        quantity = 0;
                        break;
                    }
                }
            }
        }
        return quantity;
    }

};

int main() {
    constexpr static std::string_view BUY{ "BUY" };
    constexpr static std::string_view SELL{ "SELL" };
    constexpr static std::string_view MODIFY{ "MODIFY" };
    constexpr static std::string_view CANCEL{ "CANCEL" };

    Engine engine{};

    std::string input;
    while (std::cin >> input) {
        if (input == BUY || input == SELL) {
            int price, quantity;
            std::string id;

            std::cin >> price;
            std::cin >> quantity;
            std::cin >> id;

            engine.new_order(input == BUY, price, quantity, id);
        }
        else if (input == MODIFY) {
            std::string id, side;
            int price, quantity;
            std::cin >> id;
            std::cin >> side;
            std::cin >> price;
            std::cin >> quantity;

            engine.modify(id, side == BUY, price, quantity);
        }
        else if (input == CANCEL) {
            std::string id;
            std::cin >> id;

            engine.cancel(id);
        }
    }

    return 0;
}