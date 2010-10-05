module Main
    where

import Directory
import List
import Monad
import Data.Tree
import System.IO
import System.Environment

notDDD file = file /= "." && file /= ".."

subNodes :: FilePath -> IO ([FilePath])
subNodes path = do
  files <- getDirectoryContents path
  let dirs = filter notDDD files
  return dirs

isMusicFile :: String -> Bool
isMusicFile filename = True

dirTree :: FilePath -> IO [FilePath]
dirTree path = do
  mrBool <- doesDirectoryExist path
  if mrBool
    then do
      dirs <- subNodes path
      fullPathDirs <- mapM (dirTree.(\x -> path ++ "/" ++ x)) dirs
      subTrees <- return $ foldr (++) [] fullPathDirs
      return $  subTrees
    else do
      if ".m3u" `isSuffixOf` path
        then do
          let lastSlash = last $ elemIndices '/' path
          let parent = take lastSlash path
          fd <- openFile path ReadMode
          contents <- hGetContents fd
          return $ map (parent ++) $ lines contents
        else
          return $ [path]

main = do
  argv <- getArgs
  mrTree <- dirTree $ argv !! 0
  putStrLn $ unlines $ nub mrTree

  
