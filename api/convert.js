
export default function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "POST only" });
  }
  return res.status(200).json({ message: "File received (demo only)" });
}
