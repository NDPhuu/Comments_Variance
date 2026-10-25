import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import "../styles/landing.css";

/** Case minh họa cho các mảnh giao diện trên trang. Số liệu dựng để trình bày,
 *  không phải case thật — thay bằng case thật trước khi mang đi bảo vệ. */
const CASE = {
  title: "Sửa chữa & Bảo trì · Khu B · 2026-07",
  budget: "120.000",
  actual: "168.400",
  variance: "+48.400",
};

const SECTIONS = [
  { id: "van-de", label: "Vấn đề" },
  { id: "giai-phap", label: "Giải pháp" },
  { id: "huong-dan", label: "Hướng dẫn" },
  { id: "test", label: "Thử ba chế độ" },
  { id: "so-lieu", label: "Số liệu" },
  { id: "han-che", label: "Hạn chế" },
];

const GATES = [
  ["Cổng số liệu", "Mọi con số trong bài phải khớp với engine hoặc với tài liệu đã trích."],
  ["Cổng trích dẫn", "Mã tài liệu phải tồn tại, đúng khu, và kỳ không vượt quá tháng của case."],
  ["Cổng nhận định", "Mỗi nguyên nhân xác nhận phải có ít nhất một trích dẫn hợp lệ đỡ phía sau."],
  ["Cổng từ chối", "Không có tài liệu liên kết thì hệ thống không được phép nêu nguyên nhân."],
];

const STEPS = [
  ["Chọn case", "Lọc theo mức trọng yếu và theo khu."],
  ["Đọc bằng chứng", "Xem các chứng từ đã truy xuất."],
  ["Sinh giải trình", "Mô hình viết bản nháp."],
  ["Xem kết quả kiểm", "Bốn cổng chấm lại bản nháp."],
  ["Quyết định", "Duyệt, sửa, hoặc trả lại."],
];

function CaseNums() {
  return (
    <dl className="lp-card-nums">
      <div>
        <dt>Ngân sách</dt>
        <dd>{CASE.budget}</dd>
      </div>
      <div>
        <dt>Thực tế</dt>
        <dd>{CASE.actual}</dd>
      </div>
      <div>
        <dt>Chênh lệch</dt>
        <dd>{CASE.variance}</dd>
      </div>
    </dl>
  );
}

export default function LandingPage() {
  const [active, setActive] = useState<string | null>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const tocRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;

    // Bám theo cuộn để biết đang đọc phần nào. Không unobserve — phải chạy
    // suốt cả lượt cuộn lên lẫn xuống.
    const spy = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActive(e.target.id);
        });
      },
      { rootMargin: "-20% 0px -70% 0px", threshold: 0 },
    );

    root.querySelectorAll("section[id]").forEach((s) => spy.observe(s));

    // Lớp chuyển động. Đánh dấu bằng JS để khi không có JS thì nội dung đứng
    // yên ở đúng chỗ của nó thay vì bị dịch mãi mãi.
    const rise = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          e.target.classList.add("is-in");
          rise.unobserve(e.target);
        });
      },
      { rootMargin: "0px 0px -10% 0px", threshold: 0.1 },
    );

    const RISING =
      ".lp-hero-state, .lp-hero-side, .lp-hero-cta, .lp-pain, .lp-gates," +
      " .lp-steps, .lp-figure, .lp-figs > div, .lp-lim-list, .lp-lim-para," +
      " .lp-ch-left, .lp-ch-right, .lp-band-text, .lp table";

    root.querySelectorAll(RISING).forEach((el, i) => {
      el.setAttribute("data-rise", "");
      (el as HTMLElement).style.setProperty("--d", `${(i % 3) * 70}ms`);
      rise.observe(el);
    });

    return () => {
      spy.disconnect();
      rise.disconnect();
    };
  }, []);

  // Trên điện thoại mục lục cuộn ngang, nên mục đang đọc phải tự trượt vào giữa.
  useEffect(() => {
    if (!active || !tocRef.current) return;
    const link = tocRef.current.querySelector(`a[href="#${active}"]`);
    link?.scrollIntoView({ inline: "center", block: "nearest" });
  }, [active]);

  return (
    <div className="lp" ref={rootRef}>
      {/* ---------------- HERO ---------------- */}
      <header className="lp-hero">
        <div className="lp-top">
          <div className="lp-wrap lp-top-inner">
            <Link to="/" className="lp-mark">
              Variance Workbench
            </Link>
            <Link to="/workbench" className="lp-btn">
              Mở Workbench
            </Link>
          </div>
        </div>

        <div className="lp-masthead">
          <img
            src="/assets/bw-xuong-trong.jpg"
            width={1200}
            height={675}
            alt="Bên trong một nhà xưởng công nghiệp trống, khung thép và sàn bê tông."
            decoding="async"
          />
        </div>

        <div className="lp-wrap lp-hero-body">
          <div className="lp-hero-state">
            <h1>
              Thiếu bằng chứng,
              <br />
              không kết luận.
            </h1>
          </div>
          <div className="lp-hero-side">
            <p>
              Hệ thống viết giải trình chênh lệch ngân sách cho FP&amp;A. Mỗi con
              số và mỗi nguyên nhân phải qua bốn cổng kiểm chứng trước khi hiện
              ra.
            </p>
          </div>
          <div className="lp-hero-cta">
            <a className="lp-btn" href="#test">
              Xem thử một case
            </a>
            <a className="lp-btn lp-btn-ghost" href="#van-de">
              Bắt đầu từ vấn đề
            </a>
          </div>
        </div>
      </header>

      {/* ---------------- MỤC LỤC ---------------- */}
      <nav className="lp-toc" aria-label="Mục lục trang">
        <div className="lp-wrap lp-toc-inner">
          <span className="lp-toc-mark">Variance Workbench</span>
          <div className="lp-toc-list" ref={tocRef}>
            {SECTIONS.map((s) => (
              <a
                key={s.id}
                href={`#${s.id}`}
                aria-current={active === s.id ? "true" : undefined}
              >
                {s.label}
              </a>
            ))}
          </div>
          <Link to="/workbench" className="lp-btn">
            Mở Workbench
          </Link>
        </div>
      </nav>

      {/* ---------------- 1. VẤN ĐỀ ---------------- */}
      <section className="lp-problem" id="van-de">
        <div className="lp-wrap">
          <h2 className="lp-sec-head">Vấn đề</h2>
          <p className="lp-lead">
            Giải trình chênh lệch tốn thời gian không phải vì khó viết, mà vì khó
            chứng minh.
          </p>

          <div className="lp-pains">
            <div className="lp-pain">
              <h3>Thời gian nằm ở chỗ đối chiếu</h3>
              <p>
                Mỗi kỳ đóng sổ có hàng trăm khoản lệch, và phần lớn công sức trôi
                vào việc tìm đúng chứng từ cho từng khoản.
              </p>
            </div>
            <div className="lp-pain">
              <h3>Viết trôi chảy nhưng không kiểm được</h3>
              <p>
                Bản giải trình do mô hình sinh ra đọc rất thuyết phục, nhưng không
                ai biết con số lấy từ đâu.
              </p>
            </div>
            <div className="lp-pain">
              <h3>Một nguyên nhân sai đi thẳng vào báo cáo</h3>
              <p>
                Giải trình là đầu vào của quyết định phân bổ ngân sách, nên sai
                nguyên nhân là sai quyết định.
              </p>
            </div>
          </div>

          <figure className="lp-figure">
            <img
              src="/assets/bw-toan-canh.jpg"
              width={756}
              height={425}
              loading="lazy"
              decoding="async"
              alt="Toàn cảnh một khu công nghiệp nhìn từ trên cao, các nhà xưởng xếp thành dãy."
            />
            <figcaption>
              Mỗi khu, mỗi nhà xưởng là một dòng trong P&amp;L. Chênh lệch và bằng
              chứng đều nằm ở cấp đó.
            </figcaption>
          </figure>
        </div>
      </section>

      {/* ---------------- 2. GIẢI PHÁP ---------------- */}
      <section className="lp-solution" id="giai-phap">
        <div className="lp-wrap">
          <h2 className="lp-sec-head">Giải pháp: bốn cổng kiểm chứng</h2>
          <p className="lp-lead">
            Mô hình vẫn viết. Nhưng kết quả phải đi qua bốn phép kiểm tất định
            trước khi được dán nhãn. Không phép nào dùng mô hình ngôn ngữ.
          </p>

          <div className="lp-gates" data-ui>
            {GATES.map(([name, rule]) => (
              <div className="lp-gate" key={name}>
                <h3>{name}</h3>
                <p>{rule}</p>
                <span className="lp-pass">đạt</span>
              </div>
            ))}
            <p className="lp-gates-foot">
              Bốn cổng đạt thì dán <b>verified</b>. Một cổng trượt là{" "}
              <b>flagged</b>. Từ chối đúng lúc là <b>abstained</b>. Model, phiên
              bản prompt và kết quả từng cổng đều được lưu cùng bản giải trình.
            </p>
          </div>
        </div>
      </section>

      {/* ---------------- 3. HƯỚNG DẪN ---------------- */}
      <section id="huong-dan">
        <div className="lp-wrap">
          <h2 className="lp-sec-head">Hướng dẫn: năm bước trong Workbench</h2>
          <p className="lp-lead">
            Đây đúng là thanh tiến trình bạn sẽ thấy trong ứng dụng. Bạn giữ quyền
            ở bước cuối.
          </p>

          <div className="lp-steps" data-ui>
            {STEPS.map(([title, desc]) => (
              <div className="lp-step" key={title}>
                <h3>{title}</h3>
                <p>{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------------- 4. THỬ BA CHẾ ĐỘ ---------------- */}
      <section className="lp-modes" id="test">
        <div className="lp-chapter lp-ch-m0">
          <div className="lp-wrap lp-ch-grid">
            <div className="lp-ch-left">
              <h2>M0 · không có tài liệu</h2>
              <p className="lp-ch-note">
                Mô hình tự nghĩ ra nguyên nhân, không có mã tài liệu nào để lần
                lại.
              </p>
              <span className="lp-ch-verdict">flagged</span>
            </div>
            <div className="lp-ch-right">
              <div className="lp-card" data-ui>
                <div className="lp-card-head">
                  <span>{CASE.title}</span>
                  <span className="lp-muted">M0</span>
                </div>
                <CaseNums />
                <div className="lp-card-body">
                  <p>
                    Chi phí sửa chữa vượt ngân sách chủ yếu do khối lượng bảo trì
                    định kỳ tăng trong quý và do giá vật tư biến động so với dự
                    toán đầu năm.
                  </p>
                </div>
                <div className="lp-card-cites">
                  <span className="lp-chip lp-chip-bad">Không có trích dẫn</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="lp-chapter lp-ch-m1">
          <div className="lp-wrap lp-ch-grid">
            <div className="lp-ch-left">
              <h2>M1 · có tài liệu, không kiểm</h2>
              <p className="lp-ch-note">
                Đã có trích dẫn, nhưng không ai kiểm nên một mã thuộc khu khác vẫn
                lọt vào bài.
              </p>
              <span className="lp-ch-verdict">flagged</span>
            </div>
            <div className="lp-ch-right">
              <div className="lp-card" data-ui>
                <div className="lp-card-head">
                  <span>{CASE.title}</span>
                  <span className="lp-muted">M1</span>
                </div>
                <CaseNums />
                <div className="lp-card-body">
                  <p>
                    Phát sinh từ hai đợt sửa mái và hệ thống PCCC trong tháng 7,
                    theo các chứng từ bảo trì đã ghi nhận cho khu.
                  </p>
                </div>
                <div className="lp-card-cites">
                  <span className="lp-chip">EV-017</span>
                  <span className="lp-chip">EV-023</span>
                  <span className="lp-chip lp-chip-bad">EV-041 · khu khác</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="lp-chapter lp-ch-m2">
          <div className="lp-wrap lp-ch-grid">
            <div className="lp-ch-left">
              <h2>M2 · có tài liệu và kiểm chứng</h2>

              <div className="lp-switch" role="group" aria-label="Bằng chứng cho case này">
                <input type="radio" name="ev" id="ev-on" defaultChecked />
                <label htmlFor="ev-on">Có bằng chứng</label>
                <input type="radio" name="ev" id="ev-off" />
                <label htmlFor="ev-off">Rút bằng chứng</label>
              </div>

              <p className="lp-ch-note">
                <span className="lp-state-ok">
                  Cùng một case. Rút tài liệu đi để xem hệ thống đổi câu trả lời.
                </span>
                <span className="lp-state-weak">
                  Không còn tài liệu liên kết, nên hệ thống bỏ trống phần nguyên
                  nhân thay vì đoán.
                </span>
              </p>
              <span className="lp-ch-verdict">
                <span className="lp-state-ok">verified</span>
                <span className="lp-state-weak">abstained</span>
              </span>
            </div>

            <div className="lp-ch-right">
              <div className="lp-state-ok">
                <div className="lp-card" data-ui>
                  <div className="lp-card-head">
                    <span>{CASE.title}</span>
                    <span className="lp-muted">M2 · 4/4 cổng đạt</span>
                  </div>
                  <CaseNums />
                  <div className="lp-card-body">
                    <p>
                      Chênh lệch +48.400 (40,3%) đến từ hai hạng mục sửa chữa ngoài
                      kế hoạch tại Khu B trong tháng 7, cả hai đều có chứng từ
                      nghiệm thu trong kỳ.
                    </p>
                  </div>
                  <div className="lp-card-cites">
                    <span className="lp-chip">EV-017</span>
                    <span className="lp-chip">EV-023</span>
                  </div>
                </div>
              </div>

              <div className="lp-state-weak">
                <div className="lp-card" data-ui>
                  <div className="lp-card-head">
                    <span>{CASE.title}</span>
                    <span className="lp-muted">M2 · cổng từ chối chặn</span>
                  </div>
                  <CaseNums />
                  <div className="lp-card-empty">
                    Không đủ bằng chứng để nêu nguyên nhân. Phần giải trình để
                    trống và case được chuyển lại cho người phụ trách.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ---------------- 5. SỐ LIỆU ---------------- */}
      <section id="so-lieu">
        <div className="lp-wrap">
          <h2 className="lp-sec-head">Đo trên 34 case trọng yếu</h2>

          <div className="lp-figs">
            <div>
              <div className="lp-fig-n">3/3</div>
              <p>
                Ba case được dựng riêng để không có bằng chứng. Hệ thống im lặng
                cả ba lần.
              </p>
            </div>
            <div>
              <div className="lp-fig-n">100%</div>
              <p>
                Tỷ lệ phát hiện case bẫy. Không có lớp kiểm chứng thì không bắt
                được case nào.
              </p>
            </div>
            <div>
              <div className="lp-fig-n">5%</div>
              <p>
                Nhận định thiếu bằng chứng còn lại, từ 100% khi mô hình chạy một
                mình.
              </p>
            </div>
          </div>

          <table>
            <caption>Trung bình trên 34 case, 3 lượt chạy.</caption>
            <thead>
              <tr>
                <th scope="col">Chỉ số</th>
                <th scope="col">M0 · chỉ mô hình</th>
                <th scope="col">M1 · có tài liệu</th>
                <th scope="col">M2 · có kiểm chứng</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Số khớp với nguồn</td>
                <td>0,901</td>
                <td>0,960</td>
                <td>0,984</td>
              </tr>
              <tr>
                <td>Trích dẫn hợp lệ</td>
                <td>—</td>
                <td>0,935</td>
                <td>1,000</td>
              </tr>
              <tr>
                <td>
                  Nhận định thiếu bằng chứng{" "}
                  <span className="lp-lower">(thấp = tốt)</span>
                </td>
                <td>1,000</td>
                <td>0,293</td>
                <td>0,054</td>
              </tr>
              <tr>
                <td>Bắt được case bẫy</td>
                <td>0/3</td>
                <td>0/3</td>
                <td>3/3</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* ---------------- 6. HẠN CHẾ ---------------- */}
      <section className="lp-limits" id="han-che">
        <div className="lp-wrap">
          <h2 className="lp-sec-head">Hạn chế của nghiên cứu này</h2>

          <div className="lp-lim-row">
            <dl className="lp-lim-facts">
              <div>
                <dt>Dữ liệu</dt>
                <dd>34 case mô phỏng</dd>
              </div>
              <div>
                <dt>Mô hình</dt>
                <dd>gemini-3.5-flash-lite</dd>
              </div>
              <div>
                <dt>Chấm điểm</dt>
                <dd>Tự động</dd>
              </div>
            </dl>
            <p className="lp-lim-para">
              Kết quả đo trên dữ liệu mô phỏng, một mô hình, một phiên bản prompt.
              Nó cho biết lớp kiểm chứng chạy đúng trong điều kiện có kiểm soát,
              chưa phải trên sổ sách thật.
            </p>

            <div className="lp-lim-list">
              <table>
                <caption>Những chỗ nghiên cứu này chưa với tới.</caption>
                <tbody>
                  <tr><td>Số case</td><td>34</td></tr>
                  <tr><td>Nhóm tình huống</td><td>9</td></tr>
                  <tr><td>Số mô hình đã thử</td><td>1</td></tr>
                  <tr><td>Truy xuất Recall@5</td><td>100,0%</td></tr>
                  <tr><td>Truy xuất Precision@5</td><td>33,8%</td></tr>
                  <tr><td>Chuyên viên chấm mù</td><td>chưa có</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* ---------------- DẢI CUỐI ---------------- */}
      <div className="lp-band">
        <div className="lp-band-text">
          <h2>Chạy thử trên dữ liệu của bản demo</h2>
          <p>Chọn một case, đọc bằng chứng, để hệ thống viết rồi tự chấm lại nó.</p>
          <Link to="/workbench" className="lp-btn">
            Mở Workbench
          </Link>
          <p className="lp-band-note">
            Dữ liệu mô phỏng · Không dùng cho báo cáo thực tế
          </p>
        </div>
        <img
          src="/assets/bw-cua-xuat-hang.jpg"
          width={727}
          height={431}
          loading="lazy"
          decoding="async"
          alt="Dãy cửa xuất hàng của một nhà xưởng, có dốc lên và lan can vàng."
        />
      </div>

      {/* ---------------- FOOTER ---------------- */}
      <footer className="lp-footer">
        <div className="lp-wrap">
          <div className="lp-foot-links">
            <Link to="/workbench">Workbench</Link>
            <Link to="/research">Kết quả đánh giá</Link>
            <a href="#van-de">Vấn đề</a>
            <a href="#giai-phap">Giải pháp</a>
          </div>
          <div className="lp-foot-meta">
            <p>Ảnh: khu công nghiệp, tư liệu dự án.</p>
            <p>Dữ liệu mô phỏng · Không dùng cho báo cáo thực tế</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
