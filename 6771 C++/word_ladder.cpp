#include <comp6771/word_ladder.hpp>

#include <unordered_set>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <iostream>
#include <cstdlib>
#include <queue>



//////////////////////////////////////////////////////////////////////////////////////////
//                                                                                      //
// Algorithm: 1. check if the two input word are having the same size and are both      //
//           inside the lexicon, if not, return Error message and exit the program.     //
//            2. bulid an smaller lexicon based on the size of the input word, which    //
//              can shorter the BFS time.                                               //
//            3. build an multimap that store the word change step, if the to word      //
//              cannot archieve, return Error message and exit the program. if reach    //
//              the level that contain the to word, return the map;                     //
//            4. use BFS searching the map to find all the possible paths.              //
//                                                                                      //
//////////////////////////////////////////////////////////////////////////////////////////

// check if the words are match the requirement
void check_word(std::string const& from, std::string const& to,
	std::unordered_set<std::string> const& lexicon) {

	if (from.size() != to.size()) {
		std::cout << "Error: the size of two word are different";
		std::cout << std::endl;
		exit(0);
	}

	if (lexicon.find(from) == lexicon.end()) {
		std::cout << "Error: The first word did not exist";
		std::cout << std::endl;
		exit(0);
	}

	if (lexicon.find(to) == lexicon.end()) {
		std::cout << "Error: The second word did not exist";
		std::cout << std::endl;
		exit(0);
	}
}

// compare the wordA with wordB to find out if they have only one alphabet different
auto compare(std::string const& wordA, std::string const& wordB) -> bool {
	auto flag = 0;

	for (int i = 0; i < wordA.size(); i++) {
		if (wordA[i] != wordB[i]) {
			flag++;
		}
	}
	return flag == 1;
}

// find all the word that have the same word size with the from word, and build a temporary lexicon
auto buildLexicon(std::string const& from,
	std::unordered_set<std::string> const& lexicon)
	-> std::unordered_map<std::string, int> {
	auto temp = std::unordered_map<std::string, int>{};
	auto const from_len = from.size();

	for (auto i = lexicon.begin(); i != lexicon.end(); i++) {

		if (i->size() == from_len) {
			temp[*i] = 0;
		}
	}
	return temp;
}

//using BFS to create a Map of all the possible word in the lexicon
auto createMap(std::string const& from,
	std::string const& to,
	std::unordered_map<std::string, int> lexicon)
	-> std::unordered_multimap<std::string, std::string> {

	auto map = std::unordered_multimap<std::string, std::string>{};
	auto list = std::queue<std::string>{};					// a waiting queue to store all the words in the same level that need to be visited
	auto temp_set = std::unordered_set<std::string>{};	// a temporary set to store all the word that have been visited in the same level

	list.push(from);
	lexicon.at(from) = 1;  //mark from as visited

	while (!list.empty()) {
		for (auto i = list.size(); i > 0; i--) {
			auto temp = list.front();		// get a word to find its ladder words
			list.pop();								// remove from the waiting queue

			for (auto j : lexicon) {
				if (j.second == 1) {
					continue;	//check if word is visited
				}
				if (compare(temp, j.first)) {
					map.insert({ temp,j.first });		// if word found, insert to the map

					if (temp_set.find(j.first) == temp_set.end()) {
						temp_set.insert(j.first);
						list.push(j.first);
					}
				}
			}
		}


		for (auto k = temp_set.begin(); k != temp_set.end(); k++) {
			if (*k == to) {
				return map;
			}
			lexicon.at(*k) = 1; // mark all the word in the temporary set as visited
		}
		temp_set.clear();
	}

	std::cout << "Error: map create failure"; // if the map fail to create, meaning no path exist, so stop the program and return Error
	std::cout << std::endl;
	exit(0);

}

//Use BFS agin to find all the possible path
auto findPaths(std::string const& from,
	std::string const& to,
	std::unordered_multimap<std::string, std::string> const& map)
	-> std::vector<std::vector<std::string>>
{

	auto paths = std::vector<std::vector<std::string>>{};
	auto temp = std::queue<std::vector<std::string>>{};		// temporary queue that store the path

	temp.push({ from });

	while (!temp.empty()) {
		auto path = temp.front();	// get a path in the queue
		temp.pop();

		auto word = path.back();	// find the last word in the path and check if it reach the target word

		if (word == to) {
			paths.push_back(path);
		}

		auto ret = map.equal_range(word);	// if the last word in the path is not the target word, get the word that it can change to.
		for (auto i = ret.first; i != ret.second; ++i) {
			path.push_back(i->second);		// renew the path with the new last word
			temp.push(path);
			path.pop_back();
		}

	}
	sort(paths.begin(), paths.end());
	return paths;
}

//another method
// Algorithm : 1. use dijstra to build a map that for each key, the value contain all the word that can change form the key word.
//             2. use DFS to search the dijstra map to find all the possible paths.
//             ***still unfinished.

// auto dijstra(std::string const& from,
// 			 std::unordered_multimap<std::string, std::string> const& map)
// -> std::unordered_map<std::string, std::vector<std::string>> {

// 	auto pre = std::unordered_map<std::string, std::vector<std::string>>{};
// 	std::string s = from;
// 	auto q = std::queue<std::string>{};
// 	q.push(s);
// 	auto dis = std::unordered_map<std::string, int>{};
// 	dis[s] = 0;
// 	auto visit = std::vector<std::string>{};
// 	visit.push_back(s);
// 	while (!q.empty()) {
// 		auto temp = q.front();
// 		q.pop();
// 		auto tfind = find(visit.begin(), visit.end(), temp);
// 		if (tfind != visit.end()) {
// 			continue;
// 		}
// 		visit.push_back(temp);

// 		auto ret = map.equal_range(temp);
// 		for (auto i = ret.first; i != ret.second; ++i) {
// 			auto tar = i->second;
// 			if (dis.find(tar) == dis.end()) {
// 				dis[tar]=9999;
// 			}

// 			if (dis[tar]> dis[temp]+ 1) {
// 				dis[tar]= dis[temp] + 1;
// 				pre[tar].clear();
// 				pre[tar].push_back(temp);
// 				auto ifind = find(visit.begin(), visit.end(), tar);
// 				if (ifind == visit.end()) {
// 					q.push(tar);
// 				}
// 			}
// 			else if (dis[tar]== dis[temp] + 1) {
// 				pre[tar].push_back(temp);
// 				auto ifind = find(visit.begin(), visit.end(), tar);
// 				if (ifind == visit.end()) {
// 					q.push(tar);
// 				}
// 			}
// 		}
// 	}
// 	return pre;
// }

// void DFS(std::string from,
//          std::string to,
//          std::unordered_map<std::string, std::vector<std::string>> const& pre,
//          std::vector<std::vector<std::string>> paths ){
// 	auto temp = std::vector<std::string>{};
// 	if (from == to) {
// 		temp.push_back(to);
// 		paths.push_back(temp);
// 		temp.pop_back();
// 		return;
// 	}
// 	temp.push_back(to);
// 	if (pre.find(to) != pre.end()) {
// 		for (auto i : pre.find(to)->second) {
// 			DFS(from, i, pre, paths);
// 		}
// 	}
// 	temp.pop_back();
// }

namespace word_ladder {

	[[nodiscard]] auto generate(std::string const& from,
		std::string const& to,
		std::unordered_set<std::string> const& lexicon)
		-> std::vector<std::vector<std::string>> {

		check_word(from, to, lexicon);
		auto paths = std::vector<std::vector<std::string>>{};
		auto tmp_lexicon = buildLexicon(from, lexicon);
		auto map = createMap(from, to, tmp_lexicon);
		paths = findPaths(from, to, map);
		// for (auto i : map) {
		// 	std::cout<< i.first <<" "<< i.second <<" ";
		// std::cout<< std::endl;
		// }

		//auto pre = dijstra(from, map);
		//auto paths2 = std::vector<std::vector<std::string>>{};
		//DFS(from, to, pre, paths2);

		return paths;
	}

} // namespace word_ladder
