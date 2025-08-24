/**
 * https://leetcode.com/contest/weekly-contest-464/problems/maximum-walls-destroyed-by-robots/description/
 */

	class Solution {
		public int maxWalls(int[] robots, int[] distance, int[] walls) {
			int n = robots.length;
			int[][] rb = new int[n][];
			for(int i = 0;i < n;i++){
				rb[i] = new int[]{robots[i], distance[i]};
			}
			Arrays.sort(rb, (a, b) -> Integer.compare(a[0], b[0]));
			for(int i = 0;i < n;i++){
				robots[i] = rb[i][0];
				distance[i] = rb[i][1];
			}
			int ans = 0;
			int m = walls.length;
			int p = 0;
			for(int i = 0;i < m;i++){
				if(Arrays.binarySearch(robots, walls[i]) >= 0) {
					ans++;
				}else{
					walls[p++] = walls[i];
				}
			}

			walls = Arrays.copyOf(walls, p);

			Arrays.sort(walls);
			long l = 0, r = 0;
			for(int i = 0;i < n;i++){
				int x = robots[i];
				int d = distance[i];

				int ln = lowerBound(walls, x) - lowerBound(walls, Math.max(i-1 >= 0 ? robots[i-1] : Integer.MIN_VALUE / 2, x - d - 1));
				int rn = lowerBound(walls, Math.min(i+1 < n ? robots[i+1] - 1 : Integer.MAX_VALUE / 2, x + d)) - lowerBound(walls, x - 1);
				int lwn = Math.max(0, lowerBound(walls, x) - lowerBound(walls, Math.max(i-1 >= 0 ? robots[i-1] + distance[i-1] : Integer.MIN_VALUE / 2, x - d - 1)));

				long nl = Math.max(l + ln, r + lwn);
				long nr = Math.max(l + rn, r + rn);
				l = nl;
				r = nr;
			}
			return (int)Math.max(l, r) + ans;
		}

		public static int lowerBound(int[] a, int v){ return lowerBound(a, 0, a.length, v); }
		public static int lowerBound(int[] a, int l, int r, int v)
		{
			v++;
			if(l > r || l < 0 || r > a.length)throw new IllegalArgumentException();
			int low = l-1, high = r;
			while(high-low > 1){
				int h = high+low>>>1;
				if(a[h] >= v){
					high = h;
				}else{
					low = h;
				}
			}
			return high;
		}

	}

/* Полезные ссылки: */
// 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. 💠Telegram №1💠 @quadd4rv1n7
// 3. 💠Telegram №2💠 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks