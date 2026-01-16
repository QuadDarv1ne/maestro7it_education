class Solution {
    public List<List<String>> findLadders(String beginWord, String endWord, List<String> wordList) {
        List<List<String>> result = new ArrayList<>();
        Set<String> wordSet = new HashSet<>(wordList);
        
        if (!wordSet.contains(endWord)) {
            return result;
        }
        
        // Уровни BFS
        Map<String, Integer> level = new HashMap<>();
        level.put(beginWord, 0);
        
        // Граф предшественников
        Map<String, List<String>> parents = new HashMap<>();
        
        // Очередь для BFS
        Queue<String> queue = new LinkedList<>();
        queue.offer(beginWord);
        
        boolean found = false;
        int depth = 0;
        
        while (!queue.isEmpty() && !found) {
            depth++;
            int size = queue.size();
            Set<String> visitedThisLevel = new HashSet<>();
            
            for (int i = 0; i < size; i++) {
                String currentWord = queue.poll();
                
                char[] chars = currentWord.toCharArray();
                for (int j = 0; j < chars.length; j++) {
                    char original = chars[j];
                    
                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == original) continue;
                        
                        chars[j] = c;
                        String newWord = new String(chars);
                        
                        if (newWord.equals(endWord)) {
                            parents.computeIfAbsent(endWord, k -> new ArrayList<>())
                                  .add(currentWord);
                            found = true;
                        } else if (wordSet.contains(newWord)) {
                            if (!level.containsKey(newWord)) {
                                level.put(newWord, depth);
                                queue.offer(newWord);
                                parents.computeIfAbsent(newWord, k -> new ArrayList<>())
                                      .add(currentWord);
                                visitedThisLevel.add(newWord);
                            } else if (level.get(newWord) == depth) {
                                parents.get(newWord).add(currentWord);
                            }
                        }
                    }
                    chars[j] = original;
                }
            }
            
            // Удаляем посещенные слова
            wordSet.removeAll(visitedThisLevel);
        }
        
        if (!found) return result;
        
        // Восстанавливаем пути
        List<String> path = new ArrayList<>();
        path.add(endWord);
        dfs(endWord, beginWord, parents, path, result);
        
        return result;
    }
    
    private void dfs(String currentWord, String beginWord,
                    Map<String, List<String>> parents,
                    List<String> path, List<List<String>> result) {
        if (currentWord.equals(beginWord)) {
            List<String> validPath = new ArrayList<>(path);
            Collections.reverse(validPath);
            result.add(validPath);
            return;
        }
        
        List<String> preds = parents.get(currentWord);
        if (preds != null) {
            for (String pred : preds) {
                path.add(pred);
                dfs(pred, beginWord, parents, path, result);
                path.remove(path.size() - 1);
            }
        }
    }
}